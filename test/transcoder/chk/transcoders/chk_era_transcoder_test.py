from richchk.model.chk.era.decoded_era_section import DecodedEraSection
from richchk.transcoder.chk.transcoders.chk_era_transcoder import ChkEraTranscoder

from ....chk_resources import CHK_SECTION_FILE_PATHS

_EXPECTED_TILESET = 4  # Jungle


def _read_chk_section() -> bytes:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedEraSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return chk_binary_data


def test_it_decodes_expected_tileset():
    transcoder = ChkEraTranscoder()
    chk_binary_data = _read_chk_section()
    section = transcoder.decode(chk_binary_data)
    assert section.tileset == _EXPECTED_TILESET


def test_it_decodes_and_encodes_without_changing_data():
    transcoder = ChkEraTranscoder()
    chk_binary_data = _read_chk_section()
    section = transcoder.decode(chk_binary_data)
    actual_encoded_data = transcoder.encode(section, include_header=False)
    assert actual_encoded_data == chk_binary_data
    assert transcoder.decode(actual_encoded_data) == transcoder.decode(chk_binary_data)
