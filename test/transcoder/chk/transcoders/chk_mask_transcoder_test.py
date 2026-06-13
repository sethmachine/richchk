from richchk.model.chk.mask.decoded_mask_section import DecodedMaskSection
from richchk.transcoder.chk.transcoders.chk_mask_transcoder import ChkMaskTranscoder

from ....chk_resources import CHK_SECTION_FILE_PATHS

_EXPECTED_NUM_BYTES = 128 * 128


def _read_chk_section() -> bytes:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedMaskSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return chk_binary_data


def test_it_decodes_expected_fog_data_length():
    transcoder = ChkMaskTranscoder()
    chk_binary_data = _read_chk_section()
    section = transcoder.decode(chk_binary_data)
    assert len(section.fog_data) == _EXPECTED_NUM_BYTES


def test_it_decodes_and_encodes_without_changing_data():
    transcoder = ChkMaskTranscoder()
    chk_binary_data = _read_chk_section()
    section = transcoder.decode(chk_binary_data)
    actual_encoded_data = transcoder.encode(section, include_header=False)
    assert actual_encoded_data == chk_binary_data
    assert transcoder.decode(actual_encoded_data) == transcoder.decode(chk_binary_data)
