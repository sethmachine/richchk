import os
import platform

from richchk.mpq.stormlib.stormlib_helper import StormLibHelper

from ...chk_resources import MACOS_STORMLIB_M1


def _run_test_if_mac_m1() -> bool:
    return (
        platform.system().lower() == "darwin" and platform.machine().lower() == "arm64"
    )


def test_it_create_stormlib_wrapper_from_embedded_dll():
    if _run_test_if_mac_m1():
        stormlib = StormLibHelper.load_stormlib(path_to_stormlib_dll=None)
        assert os.path.exists(stormlib.stormlib.path_to_stormlib.path_to_stormlib_dll)


def test_it_create_stormlib_wrapper_from_provided_dll():
    if _run_test_if_mac_m1():
        stormlib = StormLibHelper.load_stormlib(path_to_stormlib_dll=MACOS_STORMLIB_M1)
        assert os.path.exists(stormlib.stormlib.path_to_stormlib.path_to_stormlib_dll)
