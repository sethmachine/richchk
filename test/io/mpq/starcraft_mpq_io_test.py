import shutil
import uuid

import pytest

from richchk.editor.richchk.rich_chk_editor import RichChkEditor
from richchk.editor.richchk.rich_trig_editor import RichTrigEditor
from richchk.io.mpq.starcraft_audio_files_metadata_io import (
    StarCraftAudioFilesMetadataIo,
)
from richchk.io.mpq.starcraft_mpq_io import StarCraftMpqIo
from richchk.io.richchk.query.chk_query_util import ChkQueryUtil
from richchk.model.richchk.rich_chk import RichChk
from richchk.model.richchk.trig.actions.play_wav_action import PlayWavAction
from richchk.model.richchk.trig.conditions.always_condition import AlwaysCondition
from richchk.model.richchk.trig.player_id import PlayerId
from richchk.model.richchk.trig.rich_trig_section import RichTrigSection
from richchk.model.richchk.trig.rich_trigger import RichTrigger
from richchk.util.fileutils import CrossPlatformSafeTemporaryNamedFile

from ...chk_resources import EXAMPLE_STARCRAFT_SCM_MAP, EXAMPLE_STARCRAFT_SCX_MAP

# the canonical place the CHK is stored in a SCX/SCM map file
_CHK_MPQ_PATH = "staredit\\scenario.chk"


@pytest.mark.usefixtures("embedded_stormlib")
@pytest.fixture(scope="function")
def mpq_io(embedded_stormlib):
    if embedded_stormlib:
        return StarCraftMpqIo(embedded_stormlib)


@pytest.mark.usefixtures("embedded_stormlib")
@pytest.fixture(scope="function")
def wav_metadata_io(embedded_stormlib):
    if embedded_stormlib:
        return StarCraftAudioFilesMetadataIo(embedded_stormlib)


def _read_file_as_bytes(infile: str) -> bytes:
    with open(infile, "rb") as f:
        return f.read()


def test_it_reads_rich_chk_from_mpq(mpq_io):
    if mpq_io:
        with CrossPlatformSafeTemporaryNamedFile() as temp_scx_file:
            shutil.copy(EXAMPLE_STARCRAFT_SCX_MAP, temp_scx_file)
            # importantly reading the same MPQ file does not change any data
            chk_first_read = mpq_io.read_chk_from_mpq(temp_scx_file)
            chk_second_read = mpq_io.read_chk_from_mpq(temp_scx_file)
            assert chk_first_read == chk_second_read


def test_it_throws_when_reading_if_mpq_file_does_not_exist(mpq_io):
    if mpq_io:
        with pytest.raises(FileNotFoundError):
            mpq_io.read_chk_from_mpq(f"{uuid.uuid4()}-some-file.scx")


def test_adding_same_chk_does_not_change_data(mpq_io):
    if mpq_io:
        with (
            CrossPlatformSafeTemporaryNamedFile() as temp_scx_file,
            CrossPlatformSafeTemporaryNamedFile() as temp_scx_new_mpq,
        ):
            shutil.copy(EXAMPLE_STARCRAFT_SCX_MAP, temp_scx_file)
            chk_before_add = mpq_io.read_chk_from_mpq(temp_scx_file)
            mpq_io.save_chk_to_mpq(
                chk_before_add,
                temp_scx_file,
                temp_scx_new_mpq,
                overwrite_existing=True,
            )
            chk_after_add = mpq_io.read_chk_from_mpq(temp_scx_new_mpq)
            assert chk_before_add == chk_after_add


def test_it_adds_and_replaces_ckh_in_mpq(mpq_io):
    if mpq_io:
        with (
            CrossPlatformSafeTemporaryNamedFile() as temp_scx_file,
            CrossPlatformSafeTemporaryNamedFile() as temp_scm_file,
        ):
            shutil.copy(EXAMPLE_STARCRAFT_SCX_MAP, temp_scx_file)
            shutil.copy(EXAMPLE_STARCRAFT_SCM_MAP, temp_scm_file)
            chk_scx = mpq_io.read_chk_from_mpq(temp_scx_file)
            chk_scm = mpq_io.read_chk_from_mpq(temp_scm_file)
            assert chk_scx != chk_scm
            mpq_io.save_chk_to_mpq(
                chk_scm, temp_scm_file, temp_scx_file, overwrite_existing=True
            )
            chk_scx_replaced_with_scm = mpq_io.read_chk_from_mpq(temp_scx_file)
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
            CrossPlatformSafeTemporaryNamedFile() as temp_scx_file,
            CrossPlatformSafeTemporaryNamedFile() as temp_outfile,
        ):
            shutil.copy(EXAMPLE_STARCRAFT_SCX_MAP, temp_scx_file)
            chk_scx = mpq_io.read_chk_from_mpq(temp_scx_file)
            with pytest.raises(FileExistsError):
                mpq_io.save_chk_to_mpq(
                    chk_scx,
                    temp_scx_file,
                    temp_outfile,
                    overwrite_existing=False,
                )


def test_integration_it_adds_play_wav_action_without_duration(mpq_io, wav_metadata_io):
    # a PlayWavAction can be added if it references an existing WAV file without duration specified
    # since the duration can be pulled from the WAV metadata
    if mpq_io and wav_metadata_io:
        with (
            CrossPlatformSafeTemporaryNamedFile() as temp_scx_file,
            CrossPlatformSafeTemporaryNamedFile() as temp_scx_new_mpq,
        ):
            shutil.copy(EXAMPLE_STARCRAFT_SCX_MAP, temp_scx_file)
            chk = mpq_io.read_chk_from_mpq(temp_scx_file)
            # this wavfile exists in the CHK already
            wavfile_in_chk = "staredit\\wav\\monitor humming.1.wav"
            play_wav_trig = RichTrigger(
                _conditions=[AlwaysCondition()],
                _actions=[
                    # do not specify duration, since it will be automatically calculated when saving the CHK
                    PlayWavAction(_path_to_wav_in_mpq=wavfile_in_chk, _duration_ms=None)
                ],
                _players={PlayerId.PLAYER_1},
            )
            updated_trig = RichTrigEditor.add_triggers(
                [play_wav_trig],
                ChkQueryUtil.find_only_rich_section_in_chk(RichTrigSection, chk),
            )
            updated_chk = RichChkEditor().replace_chk_section(updated_trig, chk)
            mpq_io.save_chk_to_mpq(updated_chk, temp_scx_file, temp_scx_new_mpq, True)
            # now read back the updated CHK and verify the play wav trigger has the duration we expect
            updated_chk_again = mpq_io.read_chk_from_mpq(temp_scx_new_mpq)
            # find the play wav trigger, there's only a single one so this is safe for now
            expected_playwav_trig = [
                trig
                for trig in ChkQueryUtil.find_only_rich_section_in_chk(
                    RichTrigSection, updated_chk_again
                ).triggers
                if isinstance(trig.actions[0], PlayWavAction)
            ][0]
            play_wav_action = expected_playwav_trig.actions[0]
            assert isinstance(play_wav_action, PlayWavAction)
            assert play_wav_action.path_to_wav_in_mpq == wavfile_in_chk
            # now assert the duration is filled in as expected
            # the exact duration milliseconds of the WAV file as stored in the CHK
            expected_duration = wav_metadata_io.extract_all_audio_files_metadata(
                temp_scx_file
            )[0].duration_ms
            assert play_wav_action.duration_ms == expected_duration
