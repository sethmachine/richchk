import shutil
import tempfile
import uuid

import pytest

from richchk.io.mpq.starcraft_wav_metadata_io import StarCraftWavMetadataIo
from richchk.model.mpq.stormlib.stormlib_file_path import StormLibFilePath
from richchk.model.mpq.stormlib.wav.stormlib_wav import StormLibWav
from richchk.mpq.stormlib.stormlib_loader import StormLibLoader
from richchk.mpq.stormlib.stormlib_wrapper import StormLibWrapper

from ...chk_resources import (
    COMPLEX_STARCRAFT_SCX_MAP,
    EXAMPLE_STARCRAFT_SCM_MAP,
    MACOS_STORMLIB_M1,
)
from ...helpers.stormlib_helper import run_test_if_mac_m1

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
def wav_metadata_io(stormlib_wrapper):
    if stormlib_wrapper:
        return StarCraftWavMetadataIo(stormlib_wrapper)


def _read_file_as_bytes(infile: str) -> bytes:
    with open(infile, "rb") as f:
        return f.read()


def test_it_extracts_all_wav_metadata(wav_metadata_io):
    if wav_metadata_io:
        with tempfile.NamedTemporaryFile() as temp_scx_file:
            shutil.copy(COMPLEX_STARCRAFT_SCX_MAP, temp_scx_file.name)
            wav_metadata = wav_metadata_io.extract_all_wav_files_metadata(
                temp_scx_file.name
            )
            expected_metadata = {
                StormLibWav(_path_to_wav_in_mpq=key, _duration_ms=value)
                for (key, value) in _EXPECTED_WAV_FILE_DURATIONS_MS.items()
            }
            assert set(wav_metadata) == expected_metadata


def test_it_returns_empty_list_if_no_wav_files_present(wav_metadata_io):
    if wav_metadata_io:
        with tempfile.NamedTemporaryFile() as temp_scx_file:
            shutil.copy(EXAMPLE_STARCRAFT_SCM_MAP, temp_scx_file.name)
            wav_metadata = wav_metadata_io.extract_all_wav_files_metadata(
                temp_scx_file.name
            )
            assert wav_metadata == []


def test_it_extracts_same_metadata_multiple_times(wav_metadata_io):
    if wav_metadata_io:
        with tempfile.NamedTemporaryFile() as temp_scx_file:
            shutil.copy(COMPLEX_STARCRAFT_SCX_MAP, temp_scx_file.name)
            wav_metadata = wav_metadata_io.extract_all_wav_files_metadata(
                temp_scx_file.name
            )
            wav_metadata_again = wav_metadata_io.extract_all_wav_files_metadata(
                temp_scx_file.name
            )
            assert set(wav_metadata) == set(wav_metadata_again)


def test_it_throws_when_extracting_wav_metadata_if_mpq_does_not_exist(wav_metadata_io):
    if wav_metadata_io:
        with pytest.raises(FileNotFoundError):
            wav_metadata_io.extract_all_wav_files_metadata(
                f"{uuid.uuid4()}-some-file.scx"
            )
