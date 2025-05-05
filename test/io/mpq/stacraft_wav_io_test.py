import os.path
import shutil

import pytest

from richchk.io.mpq.starcraft_audio_files_io import StarCraftAudioFilesIo
from richchk.io.mpq.starcraft_audio_files_metadata_io import (
    StarCraftAudioFilesMetadataIo,
)
from richchk.io.mpq.starcraft_mpq_io import StarCraftMpqIo
from richchk.io.richchk.query.chk_query_util import ChkQueryUtil
from richchk.model.chk.str.decoded_str_section import DecodedStrSection
from richchk.model.mpq.stormlib.stormlib_archive_mode import StormLibArchiveMode
from richchk.model.mpq.stormlib.stormlib_file_path import StormLibFilePath
from richchk.model.richchk.rich_chk import RichChk
from richchk.model.richchk.wav.rich_wav_section import RichWavSection
from richchk.mpq.stormlib.stormlib_loader import StormLibLoader
from richchk.mpq.stormlib.stormlib_wrapper import StormLibWrapper
from richchk.util.fileutils import CrossPlatformSafeTemporaryNamedFile

from ...chk_resources import (
    EXAMPLE_OGG_FILE,
    EXAMPLE_STARCRAFT_SCX_MAP,
    EXAMPLE_WAV_FILE,
    MACOS_STORMLIB_M1,
)
from ...helpers.stormlib_test_helper import run_test_if_mac_m1

# the canonical place the CHK is stored in a SCX/SCM map file
_CHK_MPQ_PATH = "staredit\\scenario.chk"
# where WAV files are stored in a SCX/SCM map file
_WAV_MPQ_DIR = "staredit\\wav"
_WAV_FILE_EXTENSION = ".wav"


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


@pytest.fixture(scope="function")
def mpq_io(stormlib_wrapper):
    if stormlib_wrapper:
        return StarCraftMpqIo(stormlib_wrapper)


@pytest.fixture(scope="function")
def wav_io(stormlib_wrapper):
    if stormlib_wrapper:
        return StarCraftAudioFilesIo(stormlib_wrapper)


def _read_file_as_bytes(infile: str) -> bytes:
    with open(infile, "rb") as f:
        return f.read()


def test_integration_it_adds_a_wav_file_to_mpq(mpq_io, wav_io, stormlib_wrapper):
    if mpq_io and wav_io and stormlib_wrapper:
        with (
            CrossPlatformSafeTemporaryNamedFile() as temp_scx_file,
            CrossPlatformSafeTemporaryNamedFile() as new_scx_file,
        ):
            shutil.copy(EXAMPLE_STARCRAFT_SCX_MAP, temp_scx_file)
            wav_io.add_audio_files_to_mpq(
                [EXAMPLE_WAV_FILE.as_posix()],
                temp_scx_file,
                new_scx_file,
                overwrite_existing=True,
            )
            expected_wav_file_in_mpq = _build_expected_wav_mpq_path(
                EXAMPLE_WAV_FILE.as_posix()
            )
            chk = mpq_io.read_chk_from_mpq(new_scx_file)
            _assert_chk_has_wav_data(expected_wav_file_in_mpq, chk)
            _assert_wav_metadata_exists(
                expected_wav_file_in_mpq, new_scx_file, stormlib_wrapper
            )
            _assert_wav_file_exists_in_mpq(
                EXAMPLE_WAV_FILE.as_posix(),
                expected_wav_file_in_mpq,
                new_scx_file,
                stormlib_wrapper,
            )


def test_integration_it_adds_an_ogg_file_to_mpq(mpq_io, wav_io, stormlib_wrapper):
    if mpq_io and wav_io and stormlib_wrapper:
        with (
            CrossPlatformSafeTemporaryNamedFile() as temp_scx_file,
            CrossPlatformSafeTemporaryNamedFile() as new_scx_file,
        ):
            shutil.copy(EXAMPLE_STARCRAFT_SCX_MAP, temp_scx_file)
            wav_io.add_audio_files_to_mpq(
                [EXAMPLE_OGG_FILE.as_posix()],
                temp_scx_file,
                new_scx_file,
                overwrite_existing=True,
            )
            expected_wav_file_in_mpq = _build_expected_wav_mpq_path(
                EXAMPLE_OGG_FILE.as_posix()
            )
            chk = mpq_io.read_chk_from_mpq(new_scx_file)
            _assert_chk_has_wav_data(expected_wav_file_in_mpq, chk)
            _assert_wav_metadata_exists(
                expected_wav_file_in_mpq, new_scx_file, stormlib_wrapper
            )
            _assert_wav_file_exists_in_mpq(
                EXAMPLE_OGG_FILE.as_posix(),
                expected_wav_file_in_mpq,
                new_scx_file,
                stormlib_wrapper,
            )


def _build_expected_wav_mpq_path(wav_file_on_disk: str) -> str:
    return _WAV_MPQ_DIR + "\\" + os.path.basename(wav_file_on_disk)


def _assert_chk_has_wav_data(wav_file_path_in_mpq: str, chk: RichChk):
    rich_wav = ChkQueryUtil.find_only_rich_section_in_chk(RichWavSection, chk)
    rich_wavs_as_strings = {x.path_in_chk.value for x in rich_wav.wavs}
    assert wav_file_path_in_mpq in rich_wavs_as_strings
    decoded_str = ChkQueryUtil.find_only_decoded_section_in_chk(DecodedStrSection, chk)
    assert wav_file_path_in_mpq in decoded_str.strings


def _assert_wav_file_exists_in_mpq(
    wav_file_on_disk: str,
    wav_file_in_mpq: str,
    path_to_mpq_file: str,
    stormlib_wrapper: StormLibWrapper,
):
    with (CrossPlatformSafeTemporaryNamedFile() as temp_wav_file_copy_from_mpq):
        wav_bytes_on_disk = _read_file_as_bytes(wav_file_on_disk)
        open_archive_result = stormlib_wrapper.open_archive(
            path_to_mpq_file, archive_mode=StormLibArchiveMode.STORMLIB_WRITE_ONLY
        )
        stormlib_wrapper.extract_file(
            open_archive_result,
            wav_file_in_mpq,
            temp_wav_file_copy_from_mpq,
            overwrite_existing=True,
        )
        stormlib_wrapper.close_archive(open_archive_result)
        wav_bytes_from_mpq = _read_file_as_bytes(temp_wav_file_copy_from_mpq)
        assert wav_bytes_on_disk == wav_bytes_from_mpq


def _assert_wav_metadata_exists(
    wav_file_in_mpq: str, path_to_mpq_file: str, stormlib_wrapper: StormLibWrapper
):
    wav_metadata = {
        x.path_to_wav_in_mpq: x
        for x in StarCraftAudioFilesMetadataIo(
            stormlib_wrapper
        ).extract_all_audio_files_metadata(path_to_mpq_file)
    }
    assert wav_file_in_mpq in wav_metadata
