from richchk.model.chk.isom.decoded_isom_section import DecodedIsomSection
from richchk.transcoder.chk.transcoders.chk_isom_transcoder import ChkIsomTranscoder

from ....chk_resources import CHK_SECTION_FILE_PATHS

_EXPECTED_NUM_VALUES = ((128 // 2 + 1) * (128 + 1)) * 4


def _read_chk_section() -> bytes:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedIsomSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return chk_binary_data


def test_it_decodes_expected_data_length():
    transcoder = ChkIsomTranscoder()
    chk_binary_data = _read_chk_section()
    section = transcoder.decode(chk_binary_data)
    assert len(section.data) == _EXPECTED_NUM_VALUES


def test_it_decodes_and_encodes_without_changing_data():
    transcoder = ChkIsomTranscoder()
    chk_binary_data = _read_chk_section()
    section = transcoder.decode(chk_binary_data)
    actual_encoded_data = transcoder.encode(section, include_header=False)
    assert actual_encoded_data == chk_binary_data
    assert transcoder.decode(actual_encoded_data) == transcoder.decode(chk_binary_data)
