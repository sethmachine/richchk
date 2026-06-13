from richchk.model.chk.thg2.decoded_thg2_section import DecodedThg2Section
from richchk.transcoder.chk.transcoders.chk_thg2_transcoder import ChkThg2Transcoder

from ....chk_resources import CHK_SECTION_FILE_PATHS


def _read_chk_section() -> bytes:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedThg2Section.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return chk_binary_data


def test_it_decodes_empty_section():
    transcoder = ChkThg2Transcoder()
    chk_binary_data = _read_chk_section()
    section = transcoder.decode(chk_binary_data)
    assert len(section.entries) == 0


def test_it_decodes_and_encodes_without_changing_data():
    transcoder = ChkThg2Transcoder()
    chk_binary_data = _read_chk_section()
    section = transcoder.decode(chk_binary_data)
    actual_encoded_data = transcoder.encode(section, include_header=False)
    assert actual_encoded_data == chk_binary_data
    assert transcoder.decode(actual_encoded_data) == transcoder.decode(chk_binary_data)
