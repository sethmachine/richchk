import os
import shutil
import uuid

import pytest

from richchk.model.mpq.stormlib.stormlib_archive_mode import StormLibArchiveMode
from richchk.model.mpq.stormlib.stormlib_mpq_handle import StormLibMpqHandle
from richchk.model.mpq.stormlib.stormlib_operation_result import StormLibOperationResult
from richchk.util.fileutils import CrossPlatformSafeTemporaryNamedFile

from ...chk_resources import EXAMPLE_STARCRAFT_SCX_MAP

# the canonical place the CHK is stored in a SCX/SCM map file
_CHK_MPQ_PATH = "staredit\\scenario.chk"


def _read_file_as_bytes(infile: str) -> bytes:
    with open(infile, "rb") as f:
        return f.read()


@pytest.mark.usefixtures("embedded_stormlib")
def test_it_opens_and_closes_scx_map_unchanged_in_read_mode(embedded_stormlib):
    if embedded_stormlib:
        with CrossPlatformSafeTemporaryNamedFile() as temp_scx_file:
            shutil.copyfile(EXAMPLE_STARCRAFT_SCX_MAP, temp_scx_file)
            map_bytes_before_open = _read_file_as_bytes(temp_scx_file)
            open_result = embedded_stormlib.open_archive(
                temp_scx_file,
                archive_mode=StormLibArchiveMode.STORMLIB_READ_ONLY,
            )
            embedded_stormlib.close_archive(open_result)
            assert map_bytes_before_open == _read_file_as_bytes(temp_scx_file)


@pytest.mark.usefixtures("embedded_stormlib")
def test_it_opens_and_closes_scx_map_unchanged_in_write_mode(embedded_stormlib):
    if embedded_stormlib:
        with CrossPlatformSafeTemporaryNamedFile() as temp_scx_file:
            shutil.copyfile(EXAMPLE_STARCRAFT_SCX_MAP, temp_scx_file)
            map_bytes_before_open = _read_file_as_bytes(temp_scx_file)
            open_result = embedded_stormlib.open_archive(
                temp_scx_file,
                archive_mode=StormLibArchiveMode.STORMLIB_WRITE_ONLY,
            )
            embedded_stormlib.close_archive(open_result)
            assert map_bytes_before_open == _read_file_as_bytes(temp_scx_file)


@pytest.mark.usefixtures("embedded_stormlib")
def test_it_throws_if_input_file_is_not_mpq(embedded_stormlib):
    if embedded_stormlib:
        with CrossPlatformSafeTemporaryNamedFile() as temp_scx_file:
            with pytest.raises(ValueError):
                embedded_stormlib.open_archive(
                    temp_scx_file,
                    archive_mode=StormLibArchiveMode.STORMLIB_READ_ONLY,
                )


@pytest.mark.usefixtures("embedded_stormlib")
def test_it_throws_if_input_file_does_not_exist(embedded_stormlib):
    if embedded_stormlib:
        not_a_real_file = str(uuid.uuid4())
        with pytest.raises(AssertionError):
            embedded_stormlib.open_archive(
                not_a_real_file,
                archive_mode=StormLibArchiveMode.STORMLIB_READ_ONLY,
            )


@pytest.mark.usefixtures("embedded_stormlib")
def test_it_throws_if_closing_an_archive_never_opened(embedded_stormlib):
    if embedded_stormlib:
        with pytest.raises(ValueError):
            embedded_stormlib.close_archive(
                StormLibOperationResult(StormLibMpqHandle(), _result=1)
            )


@pytest.mark.usefixtures("embedded_stormlib")
def test_it_extracts_chk_from_scx_file(embedded_stormlib):
    if embedded_stormlib:
        with (
            CrossPlatformSafeTemporaryNamedFile() as temp_scx_file,
            CrossPlatformSafeTemporaryNamedFile() as temp_chk_file,
        ):
            shutil.copyfile(EXAMPLE_STARCRAFT_SCX_MAP, temp_scx_file)
            temp_chk_file_bytes_before_extract = _read_file_as_bytes(temp_scx_file)
            open_result = embedded_stormlib.open_archive(
                temp_scx_file,
                archive_mode=StormLibArchiveMode.STORMLIB_WRITE_ONLY,
            )
            embedded_stormlib.extract_file(
                open_result,
                path_to_file_in_archive=_CHK_MPQ_PATH,
                outfile=temp_chk_file,
                overwrite_existing=True,
            )
            embedded_stormlib.close_archive(open_result)
            assert os.path.exists(temp_chk_file)
            assert (
                _read_file_as_bytes(temp_chk_file) != temp_chk_file_bytes_before_extract
            )


@pytest.mark.usefixtures("embedded_stormlib")
def test_it_overwrites_existing_file_when_extracting(embedded_stormlib):
    if embedded_stormlib:
        with (
            CrossPlatformSafeTemporaryNamedFile() as temp_scx_file,
            CrossPlatformSafeTemporaryNamedFile() as temp_chk_file,
        ):
            shutil.copyfile(EXAMPLE_STARCRAFT_SCX_MAP, temp_scx_file)
            bytes_before_overwrite = b"123456"
            with open(temp_chk_file, "wb") as f:
                f.write(bytes_before_overwrite)
            open_result = embedded_stormlib.open_archive(
                temp_scx_file,
                archive_mode=StormLibArchiveMode.STORMLIB_WRITE_ONLY,
            )
            embedded_stormlib.extract_file(
                open_result,
                path_to_file_in_archive=_CHK_MPQ_PATH,
                outfile=temp_chk_file,
                overwrite_existing=True,
            )
            embedded_stormlib.close_archive(open_result)
            assert os.path.exists(temp_chk_file)
            assert _read_file_as_bytes(temp_chk_file) != bytes_before_overwrite


@pytest.mark.usefixtures("embedded_stormlib")
def test_it_throws_if_overwriting_existing_file_when_extracting(embedded_stormlib):
    if embedded_stormlib:
        with (
            CrossPlatformSafeTemporaryNamedFile() as temp_scx_file,
            CrossPlatformSafeTemporaryNamedFile() as temp_chk_file,
        ):
            shutil.copyfile(EXAMPLE_STARCRAFT_SCX_MAP, temp_scx_file)
            open_result = embedded_stormlib.open_archive(
                temp_scx_file,
                archive_mode=StormLibArchiveMode.STORMLIB_WRITE_ONLY,
            )
            with pytest.raises(FileExistsError):
                embedded_stormlib.extract_file(
                    open_result,
                    path_to_file_in_archive=_CHK_MPQ_PATH,
                    outfile=temp_chk_file,
                    overwrite_existing=False,
                )
            embedded_stormlib.close_archive(open_result)


@pytest.mark.usefixtures("embedded_stormlib")
def test_it_adds_file_to_archive(embedded_stormlib):
    if embedded_stormlib:
        with (
            CrossPlatformSafeTemporaryNamedFile() as temp_scx_file,
            CrossPlatformSafeTemporaryNamedFile() as temp_madeup_file,
            CrossPlatformSafeTemporaryNamedFile() as temp_madeup_file_extract,
        ):
            shutil.copyfile(EXAMPLE_STARCRAFT_SCX_MAP, temp_scx_file)
            madeup_file_content = b"123456"
            with open(temp_madeup_file, "wb") as f:
                f.write(madeup_file_content)
            open_result = embedded_stormlib.open_archive(
                temp_scx_file,
                archive_mode=StormLibArchiveMode.STORMLIB_WRITE_ONLY,
            )
            embedded_stormlib.add_file(open_result, temp_madeup_file, temp_madeup_file)
            embedded_stormlib.compact_archive(open_result)
            embedded_stormlib.close_archive(open_result)
            embedded_stormlib.close_archive(
                embedded_stormlib.extract_file(
                    embedded_stormlib.open_archive(
                        temp_scx_file,
                        archive_mode=StormLibArchiveMode.STORMLIB_READ_ONLY,
                    ),
                    temp_madeup_file,
                    temp_madeup_file_extract,
                    overwrite_existing=True,
                )
            )
            assert madeup_file_content == _read_file_as_bytes(temp_madeup_file_extract)


@pytest.mark.usefixtures("embedded_stormlib")
def test_it_compacts_archive(embedded_stormlib):
    if embedded_stormlib:
        with CrossPlatformSafeTemporaryNamedFile() as temp_scx_file:
            shutil.copyfile(EXAMPLE_STARCRAFT_SCX_MAP, temp_scx_file)
            open_result = embedded_stormlib.open_archive(
                temp_scx_file,
                archive_mode=StormLibArchiveMode.STORMLIB_WRITE_ONLY,
            )
            embedded_stormlib.compact_archive(open_result)
            embedded_stormlib.close_archive(open_result)
            compacted_bytes = _read_file_as_bytes(temp_scx_file)
            embedded_stormlib.close_archive(
                embedded_stormlib.compact_archive(
                    embedded_stormlib.open_archive(
                        temp_scx_file,
                        archive_mode=StormLibArchiveMode.STORMLIB_WRITE_ONLY,
                    )
                )
            )
            assert compacted_bytes == _read_file_as_bytes(temp_scx_file)
