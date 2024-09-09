import shutil
import tempfile
import uuid

import pytest

from richchk.io.mpq.starcraft_mpq_io import StarcraftMpqIo
from richchk.model.mpq.stormlib.stormlib_file_path import StormLibFilePath
from richchk.model.richchk.rich_chk import RichChk
from richchk.mpq.stormlib.stormlib_loader import StormLibLoader
from richchk.mpq.stormlib.stormlib_wrapper import StormLibWrapper

from ...chk_resources import (
    EXAMPLE_STARCRAFT_SCM_MAP,
    EXAMPLE_STARCRAFT_SCX_MAP,
    MACOS_STORMLIB_M1,
)
from ...helpers.stormlib_helper import run_test_if_mac_m1

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


@pytest.fixture(scope="function")
def mpq_io(stormlib_wrapper):
    if stormlib_wrapper:
        return StarcraftMpqIo(stormlib_wrapper)


def _read_file_as_bytes(infile: str) -> bytes:
    with open(infile, "rb") as f:
        return f.read()


def test_it_reads_rich_chk_from_mpq(mpq_io):
    if mpq_io:
        with tempfile.NamedTemporaryFile() as temp_scx_file:
            shutil.copy(EXAMPLE_STARCRAFT_SCX_MAP, temp_scx_file.name)
            # importantly reading the same MPQ file does not change any data
            chk_first_read = mpq_io.read_chk_from_mpq(temp_scx_file.name)
            chk_second_read = mpq_io.read_chk_from_mpq(temp_scx_file.name)
            assert chk_first_read == chk_second_read


def test_it_throws_when_reading_if_mpq_file_does_not_exist(mpq_io):
    if mpq_io:
        with pytest.raises(FileNotFoundError):
            mpq_io.read_chk_from_mpq(f"{uuid.uuid4()}-some-file.scx")


def test_adding_same_chk_does_not_change_data(mpq_io):
    if mpq_io:
        with (
            tempfile.NamedTemporaryFile() as temp_scx_file,
            tempfile.NamedTemporaryFile() as temp_scx_new_mpq,
        ):
            shutil.copy(EXAMPLE_STARCRAFT_SCX_MAP, temp_scx_file.name)
            chk_before_add = mpq_io.read_chk_from_mpq(temp_scx_file.name)
            mpq_io.save_chk_to_mpq(
                chk_before_add,
                temp_scx_file.name,
                temp_scx_new_mpq.name,
                overwrite_existing=True,
            )
            chk_after_add = mpq_io.read_chk_from_mpq(temp_scx_new_mpq.name)
            assert chk_before_add == chk_after_add


def test_it_adds_and_replaces_ckh_in_mpq(mpq_io):
    if mpq_io:
        with (
            tempfile.NamedTemporaryFile() as temp_scx_file,
            tempfile.NamedTemporaryFile() as temp_scm_file,
        ):
            shutil.copy(EXAMPLE_STARCRAFT_SCX_MAP, temp_scx_file.name)
            shutil.copy(EXAMPLE_STARCRAFT_SCM_MAP, temp_scm_file.name)
            chk_scx = mpq_io.read_chk_from_mpq(temp_scx_file.name)
            chk_scm = mpq_io.read_chk_from_mpq(temp_scm_file.name)
            assert chk_scx != chk_scm
            mpq_io.save_chk_to_mpq(
                chk_scm, temp_scm_file.name, temp_scx_file.name, overwrite_existing=True
            )
            chk_scx_replaced_with_scm = mpq_io.read_chk_from_mpq(temp_scx_file.name)
            assert chk_scx_replaced_with_scm == chk_scm
            assert chk_scx_replaced_with_scm != chk_scx


def test_it_throws_when_adding_file_if_base_mpq_file_does_not_exist(mpq_io):
    if mpq_io:
        with pytest.raises(FileNotFoundError):
            chk = RichChk(_chk_sections=[])
            mpq_io.save_chk_to_mpq(
                chk,
                f"{uuid.uuid4()}-some-file.scx",
                "outfile.chk",
                overwrite_existing=True,
            )


def test_it_throws_adding_chk_if_no_overwrite_and_outfile_exists(mpq_io):
    if mpq_io:
        with (
            tempfile.NamedTemporaryFile() as temp_scx_file,
            tempfile.NamedTemporaryFile() as temp_outfile,
        ):
            shutil.copy(EXAMPLE_STARCRAFT_SCX_MAP, temp_scx_file.name)
            chk_scx = mpq_io.read_chk_from_mpq(temp_scx_file.name)
            with pytest.raises(FileExistsError):
                mpq_io.save_chk_to_mpq(
                    chk_scx,
                    temp_scx_file.name,
                    temp_outfile.name,
                    overwrite_existing=False,
                )


def test_integration_it_adds_play_wav_action_without_duration(mpq_io):
    # a PlayWavAction can be added if it references an existing WAV file without duration specified
    # since the duration can be pulled from the WAV metadata
    if mpq_io:
        pass
