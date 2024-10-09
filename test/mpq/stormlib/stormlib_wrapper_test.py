import os
import shutil
import tempfile
import uuid

import pytest

from richchk.model.mpq.stormlib.stormlib_archive_mode import StormLibArchiveMode
from richchk.model.mpq.stormlib.stormlib_file_path import StormLibFilePath
from richchk.model.mpq.stormlib.stormlib_mpq_handle import StormLibMpqHandle
from richchk.model.mpq.stormlib.stormlib_operation_result import StormLibOperationResult
from richchk.mpq.stormlib.stormlib_loader import StormLibLoader
from richchk.mpq.stormlib.stormlib_wrapper import StormLibWrapper

from ...chk_resources import (
    EXAMPLE_STARCRAFT_SCX_MAP,
    LINUX_STORMLIB_X86_64,
    MACOS_STORMLIB_M1,
)
from ...helpers.stormlib_helper import run_test_if_linux_x86_64, run_test_if_mac_m1

# the canonical place the CHK is stored in a SCX/SCM map file
_CHK_MPQ_PATH = "staredit\\scenario.chk"


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
    elif run_test_if_linux_x86_64():
        return StormLibWrapper(
            StormLibLoader.load_stormlib(
                path_to_stormlib=StormLibFilePath(
                    _path_to_stormlib_dll=LINUX_STORMLIB_X86_64
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


def test_it_throws_if_input_file_does_not_exist(stormlib_wrapper):
    if stormlib_wrapper:
        not_a_real_file = str(uuid.uuid4())
        with pytest.raises(AssertionError):
            stormlib_wrapper.open_archive(
                not_a_real_file,
                archive_mode=StormLibArchiveMode.STORMLIB_READ_ONLY,
            )


def test_it_throws_if_closing_an_archive_never_opened(stormlib_wrapper):
    if stormlib_wrapper:
        with pytest.raises(ValueError):
            stormlib_wrapper.close_archive(
                StormLibOperationResult(StormLibMpqHandle(), _result=1)
            )


def test_it_extracts_chk_from_scx_file(stormlib_wrapper):
    if stormlib_wrapper:
        with (
            tempfile.NamedTemporaryFile() as temp_scx_file,
            tempfile.NamedTemporaryFile() as temp_chk_file,
        ):
            shutil.copyfile(EXAMPLE_STARCRAFT_SCX_MAP, temp_scx_file.name)
            temp_chk_file_bytes_before_extract = _read_file_as_bytes(temp_scx_file.name)
            open_result = stormlib_wrapper.open_archive(
                temp_scx_file.name,
                archive_mode=StormLibArchiveMode.STORMLIB_WRITE_ONLY,
            )
            stormlib_wrapper.extract_file(
                open_result,
                path_to_file_in_archive=_CHK_MPQ_PATH,
                outfile=temp_chk_file.name,
                overwrite_existing=True,
            )
            stormlib_wrapper.close_archive(open_result)
            assert os.path.exists(temp_chk_file.name)
            assert (
                _read_file_as_bytes(temp_chk_file.name)
                != temp_chk_file_bytes_before_extract
            )


def test_it_ovewrites_existing_file_when_extracting(stormlib_wrapper):
    if stormlib_wrapper:
        with (
            tempfile.NamedTemporaryFile() as temp_scx_file,
            tempfile.NamedTemporaryFile() as temp_chk_file,
        ):
            shutil.copyfile(EXAMPLE_STARCRAFT_SCX_MAP, temp_scx_file.name)
            bytes_before_overwrite = b"123456"
            with open(temp_chk_file.name, "wb") as f:
                f.write(bytes_before_overwrite)
            open_result = stormlib_wrapper.open_archive(
                temp_scx_file.name,
                archive_mode=StormLibArchiveMode.STORMLIB_WRITE_ONLY,
            )
            stormlib_wrapper.extract_file(
                open_result,
                path_to_file_in_archive=_CHK_MPQ_PATH,
                outfile=temp_chk_file.name,
                overwrite_existing=True,
            )
            stormlib_wrapper.close_archive(open_result)
            assert os.path.exists(temp_chk_file.name)
            assert _read_file_as_bytes(temp_chk_file.name) != bytes_before_overwrite


def test_it_throws_if_ovewriting_existing_file_when_extracting(stormlib_wrapper):
    if stormlib_wrapper:
        with (
            tempfile.NamedTemporaryFile() as temp_scx_file,
            tempfile.NamedTemporaryFile() as temp_chk_file,
        ):
            shutil.copyfile(EXAMPLE_STARCRAFT_SCX_MAP, temp_scx_file.name)
            open_result = stormlib_wrapper.open_archive(
                temp_scx_file.name,
                archive_mode=StormLibArchiveMode.STORMLIB_WRITE_ONLY,
            )
            with pytest.raises(FileExistsError):
                stormlib_wrapper.extract_file(
                    open_result,
                    path_to_file_in_archive=_CHK_MPQ_PATH,
                    outfile=temp_chk_file.name,
                    overwrite_existing=False,
                )


def test_it_adds_file_to_archive(stormlib_wrapper):
    if stormlib_wrapper:
        with (
            tempfile.NamedTemporaryFile() as temp_scx_file,
            tempfile.NamedTemporaryFile() as temp_madeup_file,
            tempfile.NamedTemporaryFile() as temp_madeup_file_extract,
        ):
            shutil.copyfile(EXAMPLE_STARCRAFT_SCX_MAP, temp_scx_file.name)
            madeup_file_content = b"123456"
            with open(temp_madeup_file.name, "wb") as f:
                f.write(madeup_file_content)
            open_result = stormlib_wrapper.open_archive(
                temp_scx_file.name,
                archive_mode=StormLibArchiveMode.STORMLIB_WRITE_ONLY,
            )
            stormlib_wrapper.add_file(
                open_result, temp_madeup_file.name, temp_madeup_file.name
            )
            stormlib_wrapper.compact_archive(open_result)
            stormlib_wrapper.close_archive(open_result)
            stormlib_wrapper.close_archive(
                stormlib_wrapper.extract_file(
                    stormlib_wrapper.open_archive(
                        temp_scx_file.name,
                        archive_mode=StormLibArchiveMode.STORMLIB_READ_ONLY,
                    ),
                    temp_madeup_file.name,
                    temp_madeup_file_extract.name,
                    overwrite_existing=True,
                )
            )
            assert madeup_file_content == _read_file_as_bytes(
                temp_madeup_file_extract.name
            )


def test_it_compacts_archive(stormlib_wrapper):
    if stormlib_wrapper:
        with tempfile.NamedTemporaryFile() as temp_scx_file:
            shutil.copyfile(EXAMPLE_STARCRAFT_SCX_MAP, temp_scx_file.name)
            open_result = stormlib_wrapper.open_archive(
                temp_scx_file.name,
                archive_mode=StormLibArchiveMode.STORMLIB_WRITE_ONLY,
            )
            stormlib_wrapper.compact_archive(open_result)
            stormlib_wrapper.close_archive(open_result)
            compacted_bytes = _read_file_as_bytes(temp_scx_file.name)
            stormlib_wrapper.close_archive(
                stormlib_wrapper.compact_archive(
                    stormlib_wrapper.open_archive(
                        temp_scx_file.name,
                        archive_mode=StormLibArchiveMode.STORMLIB_WRITE_ONLY,
                    )
                )
            )
            assert compacted_bytes == _read_file_as_bytes(temp_scx_file.name)
