from richchk.model.chk.dim.decoded_dim_section import DecodedDimSection
from richchk.transcoder.chk.transcoders.chk_dim_transcoder import ChkDimTranscoder

from ....chk_resources import CHK_SECTION_FILE_PATHS

_EXPECTED_WIDTH = 128
_EXPECTED_HEIGHT = 128


def _read_chk_section() -> bytes:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedDimSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return chk_binary_data


def test_it_decodes_expected_dimensions():
    transcoder = ChkDimTranscoder()
    chk_binary_data = _read_chk_section()
    section = transcoder.decode(chk_binary_data)
    assert section.width == _EXPECTED_WIDTH
    assert section.height == _EXPECTED_HEIGHT


def test_it_decodes_and_encodes_without_changing_data():
    transcoder = ChkDimTranscoder()
    chk_binary_data = _read_chk_section()
    section = transcoder.decode(chk_binary_data)
    actual_encoded_data = transcoder.encode(section, include_header=False)
    assert actual_encoded_data == chk_binary_data
    assert transcoder.decode(actual_encoded_data) == transcoder.decode(chk_binary_data)
