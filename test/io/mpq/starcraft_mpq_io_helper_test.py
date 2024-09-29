import platform

from richchk.io.mpq.starcraft_mpq_io_helper import StarCraftMpqIoHelper

from ...chk_resources import MACOS_STORMLIB_M1


def _run_test_if_mac_m1() -> bool:
    return (
        platform.system().lower() == "darwin" and platform.machine().lower() == "arm64"
    )


def test_it_create_mpq_io_from_embedded_dll():
    if _run_test_if_mac_m1():
        StarCraftMpqIoHelper.create_mpq_io(path_to_stormlib_dll=None)


def test_it_create_mpq_io_from_provided_dll():
    if _run_test_if_mac_m1():
        StarCraftMpqIoHelper.create_mpq_io(path_to_stormlib_dll=MACOS_STORMLIB_M1)


def test_it_create_wav_io_from_embedded_dll():
    if _run_test_if_mac_m1():
        StarCraftMpqIoHelper.create_wav_io(path_to_stormlib_dll=None)


def test_it_create_wav_io_from_provided_dll():
    if _run_test_if_mac_m1():
        StarCraftMpqIoHelper.create_wav_io(path_to_stormlib_dll=MACOS_STORMLIB_M1)


def test_it_create_wav_metadata_io_from_embedded_dll():
    if _run_test_if_mac_m1():
        StarCraftMpqIoHelper.create_wav_metadata_io(path_to_stormlib_dll=None)


def test_it_create_wav_metadata_io_from_provided_dll():
    if _run_test_if_mac_m1():
        StarCraftMpqIoHelper.create_wav_metadata_io(
            path_to_stormlib_dll=MACOS_STORMLIB_M1
        )
