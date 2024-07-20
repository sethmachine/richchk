import shutil
import tempfile

import pytest

from richchk.model.mpq.stormlib.stormlib_archive_mode import StormLibArchiveMode
from richchk.model.mpq.stormlib.stormlib_file_path import StormLibFilePath
from richchk.mpq.stormlib.stormlib_file_searcher import StormLibFileSearcher
from richchk.mpq.stormlib.stormlib_loader import StormLibLoader
from richchk.mpq.stormlib.stormlib_wrapper import StormLibWrapper

from ....chk_resources import COMPLEX_STARCRAFT_SCX_MAP, MACOS_STORMLIB_M1
from ....helpers.stormlib_helper import run_test_if_mac_m1

# the canonical place the CHK is stored in a SCX/SCM map file
_CHK_MPQ_PATH = "staredit\\scenario.chk"


EXPECTED_WAV_FILES_IN_SCX_FILE = {
    "staredit\\wav\\monitor humming.1.wav",
    "staredit\\wav\\monitor humming.2.wav",
    "staredit\\wav\\monitor humming.3.wav",
}
ALL_EXPECTED_FILES_IN_SCX_FILE = {"(listfile)", _CHK_MPQ_PATH}.union(
    EXPECTED_WAV_FILES_IN_SCX_FILE
)


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


def test_it_finds_all_files_in_scx_map(stormlib_wrapper):
    if stormlib_wrapper:
        with tempfile.NamedTemporaryFile() as temp_scx_file:
            shutil.copyfile(COMPLEX_STARCRAFT_SCX_MAP, temp_scx_file.name)
            open_result = stormlib_wrapper.open_archive(
                temp_scx_file.name,
                archive_mode=StormLibArchiveMode.STORMLIB_READ_ONLY,
            )
            searcher = StormLibFileSearcher(
                stormlib_reference=stormlib_wrapper.stormlib,
                open_mpq_handle=open_result,
            )
            all_files = searcher.find_all_files_matching_pattern(search_pattern="*")
            stormlib_wrapper.close_archive(open_result)
            assert set(all_files) == ALL_EXPECTED_FILES_IN_SCX_FILE


def test_it_finds_all_wav_files_in_scx_map(stormlib_wrapper):
    if stormlib_wrapper:
        with tempfile.NamedTemporaryFile() as temp_scx_file:
            shutil.copyfile(COMPLEX_STARCRAFT_SCX_MAP, temp_scx_file.name)
            open_result = stormlib_wrapper.open_archive(
                temp_scx_file.name,
                archive_mode=StormLibArchiveMode.STORMLIB_READ_ONLY,
            )
            searcher = StormLibFileSearcher(
                stormlib_reference=stormlib_wrapper.stormlib,
                open_mpq_handle=open_result,
            )
            wav_files = searcher.find_all_files_matching_pattern(search_pattern="*.wav")
            stormlib_wrapper.close_archive(open_result)
            assert set(wav_files) == EXPECTED_WAV_FILES_IN_SCX_FILE


def test_it_returns_empty_list_if_no_files_found(stormlib_wrapper):
    if stormlib_wrapper:
        with tempfile.NamedTemporaryFile() as temp_scx_file:
            shutil.copyfile(COMPLEX_STARCRAFT_SCX_MAP, temp_scx_file.name)
            open_result = stormlib_wrapper.open_archive(
                temp_scx_file.name,
                archive_mode=StormLibArchiveMode.STORMLIB_READ_ONLY,
            )
            searcher = StormLibFileSearcher(
                stormlib_reference=stormlib_wrapper.stormlib,
                open_mpq_handle=open_result,
            )
            found_files = searcher.find_all_files_matching_pattern(
                search_pattern="*.foof"
            )
            stormlib_wrapper.close_archive(open_result)
            assert len(found_files) == 0
            assert not found_files
