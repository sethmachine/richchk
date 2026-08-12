from richchk.model.chk.sprp.decoded_sprp_section import DecodedSprpSection
from richchk.transcoder.chk.transcoders.chk_sprp_transcoder import ChkSprpTranscoder

from ....chk_resources import CHK_SECTION_FILE_PATHS

_SPRP_SECTION_KEY = DecodedSprpSection.section_name().value
_EXPECTED_SCENARIO_NAME_STRING_ID = 1
_EXPECTED_SCENARIO_DESCRIPTION_STRING_ID = 2


def _read_chk_section() -> bytes:
    with open(CHK_SECTION_FILE_PATHS[_SPRP_SECTION_KEY], "rb") as f:
        return f.read()


def test_it_decodes_scenario_name_string_id():
    section = ChkSprpTranscoder().decode(_read_chk_section())
    assert section.scenario_name_string_id == _EXPECTED_SCENARIO_NAME_STRING_ID


def test_it_decodes_scenario_description_string_id():
    section = ChkSprpTranscoder().decode(_read_chk_section())
    assert (
        section.scenario_description_string_id
        == _EXPECTED_SCENARIO_DESCRIPTION_STRING_ID
    )


def test_it_decodes_and_encodes_without_changing_data():
    transcoder = ChkSprpTranscoder()
    chk_binary_data = _read_chk_section()
    section = transcoder.decode(chk_binary_data)
    actual_encoded_data = transcoder.encode(section, include_header=False)
    assert actual_encoded_data == chk_binary_data
    assert transcoder.decode(actual_encoded_data) == transcoder.decode(chk_binary_data)
