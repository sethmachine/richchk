import platform

from richchk.model.mpq.stormlib.stormlib_file_path import StormLibFilePath
from richchk.mpq.stormlib.stormlib_loader import StormLibLoader

from ...chk_resources import MACOS_STORMLIB_M1


def _run_test_if_mac_m1() -> bool:
    return (
        platform.system().lower() == "darwin" and platform.machine().lower() == "arm64"
    )


def test_it_loads_macos_m1_dll():
    if _run_test_if_mac_m1():
        StormLibLoader.load_stormlib(
            path_to_stormlib=StormLibFilePath(_path_to_stormlib_dll=MACOS_STORMLIB_M1)
        )
