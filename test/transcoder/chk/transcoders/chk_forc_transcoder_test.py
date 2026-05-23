from richchk.model.chk.forc.decoded_forc_section import DecodedForcSection
from richchk.transcoder.chk.transcoders.chk_forc_transcoder import ChkForcTranscoder

from ....chk_resources import CHK_SECTION_FILE_PATHS

_EXPECTED_PLAYER_FORCE_ASSIGNMENTS = [0, 0, 1, 1, 0, 0, 0, 0]
_EXPECTED_FORCE_NAME_STRING_IDS = [1, 2, 0, 0]
_EXPECTED_FORCE_FLAGS = [0x06, 0x06, 0x00, 0x00]


def _read_chk_section() -> bytes:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedForcSection.section_name().value], "rb"
    ) as f:
        return f.read()


def test_it_decodes_expected_player_force_assignments():
    transcoder = ChkForcTranscoder()
    section = transcoder.decode(_read_chk_section())
    assert section.player_force_assignments == _EXPECTED_PLAYER_FORCE_ASSIGNMENTS


def test_it_decodes_expected_force_name_string_ids():
    transcoder = ChkForcTranscoder()
    section = transcoder.decode(_read_chk_section())
    assert section.force_name_string_ids == _EXPECTED_FORCE_NAME_STRING_IDS


def test_it_decodes_expected_force_flags():
    transcoder = ChkForcTranscoder()
    section = transcoder.decode(_read_chk_section())
    assert section.force_flags == _EXPECTED_FORCE_FLAGS


def test_it_decodes_and_encodes_without_changing_data():
    transcoder = ChkForcTranscoder()
    chk_binary_data = _read_chk_section()
    section = transcoder.decode(chk_binary_data)
    actual_encoded_data = transcoder.encode(section, include_header=False)
    assert actual_encoded_data == chk_binary_data
    assert transcoder.decode(actual_encoded_data) == transcoder.decode(chk_binary_data)
