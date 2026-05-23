from richchk.model.chk.side.decoded_side_section import DecodedSideSection
from richchk.transcoder.chk.transcoders.chk_side_transcoder import ChkSideTranscoder

from ....chk_resources import CHK_SECTION_FILE_PATHS

_EXPECTED_PLAYER_RACES = [0x01, 0x00, 0x02, 0x06, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07]


def _read_chk_section() -> bytes:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedSideSection.section_name().value], "rb"
    ) as f:
        return f.read()


def test_it_decodes_expected_player_races():
    transcoder = ChkSideTranscoder()
    section = transcoder.decode(_read_chk_section())
    assert section.player_races == _EXPECTED_PLAYER_RACES


def test_it_decodes_and_encodes_without_changing_data():
    transcoder = ChkSideTranscoder()
    chk_binary_data = _read_chk_section()
    section = transcoder.decode(chk_binary_data)
    actual_encoded_data = transcoder.encode(section, include_header=False)
    assert actual_encoded_data == chk_binary_data
    assert transcoder.decode(actual_encoded_data) == transcoder.decode(chk_binary_data)
