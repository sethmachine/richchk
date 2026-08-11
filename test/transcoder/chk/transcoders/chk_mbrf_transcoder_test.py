from richchk.model.chk.mbrf.decoded_mbrf_section import DecodedMbrfSection
from richchk.model.richchk.mbrf.briefing_action_id import BriefingActionId
from richchk.transcoder.chk.transcoders.chk_mbrf_transcoder import ChkMbrfTranscoder

from ....chk_resources import CHK_SECTION_FILE_PATHS

_MBRF_SECTION_KEY = DecodedMbrfSection.section_name().value
_MBRF_MARKER_CONDITION_ID = 13


def _read_chk_section() -> bytes:
    with open(CHK_SECTION_FILE_PATHS[_MBRF_SECTION_KEY], "rb") as f:
        return f.read()


def test_it_decodes_expected_briefing_count():
    transcoder = ChkMbrfTranscoder()
    section = transcoder.decode(_read_chk_section())
    assert len(section.triggers) == 1


def test_it_decodes_mbrf_marker_condition_in_first_slot():
    transcoder = ChkMbrfTranscoder()
    section = transcoder.decode(_read_chk_section())
    briefing = section.triggers[0]
    assert briefing.conditions[0]._condition_id == _MBRF_MARKER_CONDITION_ID


def test_it_decodes_remaining_conditions_as_null():
    transcoder = ChkMbrfTranscoder()
    section = transcoder.decode(_read_chk_section())
    briefing = section.triggers[0]
    for condition in briefing.conditions[1:]:
        assert condition._condition_id == 0


def test_it_decodes_wait_action_with_correct_time():
    transcoder = ChkMbrfTranscoder()
    section = transcoder.decode(_read_chk_section())
    briefing = section.triggers[0]
    non_null_actions = [
        a for a in briefing.actions if a._action_id != BriefingActionId.NO_ACTION.id
    ]
    assert len(non_null_actions) == 1
    wait_action = non_null_actions[0]
    assert wait_action._action_id == BriefingActionId.WAIT.id
    assert wait_action._time == 555


def test_it_decodes_and_encodes_without_changing_data():
    transcoder = ChkMbrfTranscoder()
    chk_binary_data = _read_chk_section()
    section = transcoder.decode(chk_binary_data)
    actual_encoded_data = transcoder.encode(section, include_header=False)
    assert actual_encoded_data == chk_binary_data
    assert transcoder.decode(actual_encoded_data) == transcoder.decode(chk_binary_data)
