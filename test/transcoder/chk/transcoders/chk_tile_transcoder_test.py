from richchk.model.chk.tile.decoded_tile_section import DecodedTileSection
from richchk.transcoder.chk.transcoders.chk_tile_transcoder import ChkTileTranscoder

from ....chk_resources import CHK_SECTION_FILE_PATHS

_EXPECTED_NUM_TILES = 128 * 128


def _read_chk_section() -> bytes:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedTileSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return chk_binary_data


def test_it_decodes_expected_tile_count():
    transcoder = ChkTileTranscoder()
    chk_binary_data = _read_chk_section()
    section = transcoder.decode(chk_binary_data)
    assert len(section.tiles) == _EXPECTED_NUM_TILES


def test_it_decodes_and_encodes_without_changing_data():
    transcoder = ChkTileTranscoder()
    chk_binary_data = _read_chk_section()
    section = transcoder.decode(chk_binary_data)
    actual_encoded_data = transcoder.encode(section, include_header=False)
    assert actual_encoded_data == chk_binary_data
    assert transcoder.decode(actual_encoded_data) == transcoder.decode(chk_binary_data)
