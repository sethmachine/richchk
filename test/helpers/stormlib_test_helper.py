import platform
from test.chk_resources import LINUX_STORMLIB_X86_64, MACOS_STORMLIB_M1
from typing import Optional

import pytest

from richchk.model.mpq.stormlib.stormlib_file_path import StormLibFilePath
from richchk.mpq.stormlib.stormlib_loader import StormLibLoader
from richchk.mpq.stormlib.stormlib_wrapper import StormLibWrapper


def run_test_if_mac_m1() -> bool:
    return (
        platform.system().lower() == "darwin" and platform.machine().lower() == "arm64"
    )


def run_test_if_linux_x86_64() -> bool:
    return (
        platform.system().lower() == "linux" and platform.machine().lower() == "x86_64"
    )


def run_test_if_supported_os() -> bool:
    return any([run_test_if_mac_m1(), run_test_if_linux_x86_64()])


def _first_true(iterable, default=False, predicate=None):
    """Returns the first true value or the *default* if there is no true value."""
    return next(filter(predicate, iterable), default)


def _get_embedded_stormlib_path() -> Optional[str]:
    possible_stormlibs: tuple[tuple[bool, str], ...] = (
        (run_test_if_mac_m1(), str(MACOS_STORMLIB_M1)),
        (run_test_if_linux_x86_64(), str(LINUX_STORMLIB_X86_64)),
    )
    maybe_embedded_stormlib = _first_true(
        possible_stormlibs, default=None, predicate=lambda x: x[0] is True
    )
    if maybe_embedded_stormlib:
        return maybe_embedded_stormlib[1]


@pytest.fixture(scope="function")
def embedded_stormlib_path() -> Optional[str]:
    return _get_embedded_stormlib_path()


@pytest.fixture(scope="function")
def embedded_stormlib() -> Optional[StormLibWrapper]:
    embedded_stormlib_path = _get_embedded_stormlib_path()
    if embedded_stormlib_path:
        return StormLibWrapper(
            StormLibLoader.load_stormlib(
                path_to_stormlib=StormLibFilePath(
                    _path_to_stormlib_dll=embedded_stormlib_path
                )
            )
        )
