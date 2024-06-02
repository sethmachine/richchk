import ctypes
import shutil
import tempfile

import pytest

from richchk.model.mpq.stormlib.stormlib_archive_mode import StormLibArchiveMode
from richchk.model.mpq.stormlib.stormlib_file_path import StormLibFilePath
from richchk.model.mpq.stormlib.stormlib_operation_result import StormLibOperationResult
from richchk.mpq.stormlib.stormlib_loader import StormLibLoader
from richchk.mpq.stormlib.stormlib_wrapper import StormLibWrapper

from ...chk_resources import EXAMPLE_STARCRAFT_SCX_MAP, MACOS_STORMLIB_M1
from ...helpers.stormlib_helper import run_test_if_mac_m1


@pytest.fixture(scope="function")
def stormlib_wrapper():
    if run_test_if_mac_m1():
        return StormLibWrapper(
            StormLibLoader.load_stormlib(
                path_to_stormlib=StormLibFilePath(
                    _path_to_stormlib_dll=MACOS_STORMLIB_M1
                )
            )
        )


def _read_file_as_bytes(infile: str) -> bytes:
    with open(infile, "rb") as f:
        return f.read()


def test_it_opens_and_closes_scx_map_unchanged_in_read_mode(stormlib_wrapper):
    if stormlib_wrapper:
        with tempfile.NamedTemporaryFile() as temp_scx_file:
            shutil.copyfile(EXAMPLE_STARCRAFT_SCX_MAP, temp_scx_file.name)
            map_bytes_before_open = _read_file_as_bytes(temp_scx_file.name)
            open_result = stormlib_wrapper.open_archive(
                temp_scx_file.name,
                archive_mode=StormLibArchiveMode.STORMLIB_READ_ONLY,
            )
            stormlib_wrapper.close_archive(open_result)
            assert map_bytes_before_open == _read_file_as_bytes(temp_scx_file.name)


def test_it_opens_and_closes_scx_map_unchanged_in_write_mode(stormlib_wrapper):
    if stormlib_wrapper:
        with tempfile.NamedTemporaryFile() as temp_scx_file:
            shutil.copyfile(EXAMPLE_STARCRAFT_SCX_MAP, temp_scx_file.name)
            map_bytes_before_open = _read_file_as_bytes(temp_scx_file.name)
            open_result = stormlib_wrapper.open_archive(
                temp_scx_file.name,
                archive_mode=StormLibArchiveMode.STORMLIB_WRITE_ONLY,
            )
            stormlib_wrapper.close_archive(open_result)
            assert map_bytes_before_open == _read_file_as_bytes(temp_scx_file.name)


def test_it_throws_if_input_file_is_not_mpq(stormlib_wrapper):
    if stormlib_wrapper:
        with tempfile.NamedTemporaryFile() as temp_scx_file:
            with pytest.raises(ValueError):
                stormlib_wrapper.open_archive(
                    temp_scx_file.name,
                    archive_mode=StormLibArchiveMode.STORMLIB_READ_ONLY,
                )


def test_it_throws_if_closing_an_archive_never_opened(stormlib_wrapper):
    if stormlib_wrapper:
        with pytest.raises(ValueError):
            stormlib_wrapper.close_archive(
                StormLibOperationResult(ctypes.c_void_p(), _result=1)
            )
