import shutil
import uuid

import pytest

from richchk.io.mpq.starcraft_audio_files_metadata_io import (
    StarCraftAudioFilesMetadataIo,
)
from richchk.model.mpq.stormlib.stormlib_file_path import StormLibFilePath
from richchk.model.mpq.stormlib.wav.stormlib_wav import StormLibWav
from richchk.mpq.stormlib.stormlib_loader import StormLibLoader
from richchk.mpq.stormlib.stormlib_wrapper import StormLibWrapper
from richchk.util.fileutils import CrossPlatformSafeTemporaryNamedFile

from ...chk_resources import (
    COMPLEX_STARCRAFT_SCX_MAP,
    EXAMPLE_STARCRAFT_SCM_MAP,
    MACOS_STORMLIB_M1,
)
from ...helpers.stormlib_test_helper import run_test_if_mac_m1

# these are the 3 WAV files in COMPLEX_STARCRAFT_SCX_MAP
# these are the paths each WAV file is stored inside the MPQ archive
# the duration milliseconds has its decimal component completely truncated
_EXPECTED_WAV_FILE_DURATIONS_MS = {
    "staredit\\wav\\monitor humming.1.wav": 4144,
    "staredit\\wav\\monitor humming.2.wav": 3575,
    "staredit\\wav\\monitor humming.3.wav": 4527,
}


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
def audio_files_metadata_io(stormlib_wrapper):
    if stormlib_wrapper:
        return StarCraftAudioFilesMetadataIo(stormlib_wrapper)


def _read_file_as_bytes(infile: str) -> bytes:
    with open(infile, "rb") as f:
        return f.read()


def test_it_extracts_all_wav_metadata(audio_files_metadata_io):
    if audio_files_metadata_io:
        with CrossPlatformSafeTemporaryNamedFile() as temp_scx_file:
            shutil.copy(COMPLEX_STARCRAFT_SCX_MAP, temp_scx_file)
            wav_metadata = audio_files_metadata_io.extract_all_audio_files_metadata(
                temp_scx_file
            )
            expected_metadata = {
                StormLibWav(_path_to_wav_in_mpq=key, _duration_ms=value)
                for (key, value) in _EXPECTED_WAV_FILE_DURATIONS_MS.items()
            }
            assert set(wav_metadata) == expected_metadata


def test_it_returns_empty_list_if_no_wav_files_present(audio_files_metadata_io):
    if audio_files_metadata_io:
        with CrossPlatformSafeTemporaryNamedFile() as temp_scx_file:
            shutil.copy(EXAMPLE_STARCRAFT_SCM_MAP, temp_scx_file)
            wav_metadata = audio_files_metadata_io.extract_all_audio_files_metadata(
                temp_scx_file
            )
            assert wav_metadata == []


def test_it_extracts_same_metadata_multiple_times(audio_files_metadata_io):
    if audio_files_metadata_io:
        with CrossPlatformSafeTemporaryNamedFile() as temp_scx_file:
            shutil.copy(COMPLEX_STARCRAFT_SCX_MAP, temp_scx_file)
            wav_metadata = audio_files_metadata_io.extract_all_audio_files_metadata(
                temp_scx_file
            )
            wav_metadata_again = (
                audio_files_metadata_io.extract_all_audio_files_metadata(temp_scx_file)
            )
            assert set(wav_metadata) == set(wav_metadata_again)


def test_it_throws_when_extracting_wav_metadata_if_mpq_does_not_exist(
    audio_files_metadata_io,
):
    if audio_files_metadata_io:
        with pytest.raises(FileNotFoundError):
            audio_files_metadata_io.extract_all_audio_files_metadata(
                f"{uuid.uuid4()}-some-file.scx"
            )
