from richchk.model.chk.ownr.decoded_ownr_section import DecodedOwnrSection
from richchk.transcoder.chk.transcoders.chk_ownr_transcoder import ChkOwnrTranscoder

from ....chk_resources import CHK_SECTION_FILE_PATHS

_EXPECTED_PLAYER_CONTROLLERS = [
    0x06,
    0x05,
    0x03,
    0x07,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
]


def _read_chk_section() -> bytes:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedOwnrSection.section_name().value], "rb"
    ) as f:
        return f.read()


def test_it_decodes_expected_player_controllers():
    transcoder = ChkOwnrTranscoder()
    section = transcoder.decode(_read_chk_section())
    assert section.player_controllers == _EXPECTED_PLAYER_CONTROLLERS


def test_it_decodes_and_encodes_without_changing_data():
    transcoder = ChkOwnrTranscoder()
    chk_binary_data = _read_chk_section()
    section = transcoder.decode(chk_binary_data)
    actual_encoded_data = transcoder.encode(section, include_header=False)
    assert actual_encoded_data == chk_binary_data
    assert transcoder.decode(actual_encoded_data) == transcoder.decode(chk_binary_data)
