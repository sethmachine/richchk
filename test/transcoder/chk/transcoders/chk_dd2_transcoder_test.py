from richchk.model.chk.dd2.decoded_dd2_section import DecodedDd2Section
from richchk.transcoder.chk.transcoders.chk_dd2_transcoder import ChkDd2Transcoder

from ....chk_resources import CHK_SECTION_FILE_PATHS


def _read_chk_section() -> bytes:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedDd2Section.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return chk_binary_data


def test_it_decodes_empty_section():
    transcoder = ChkDd2Transcoder()
    chk_binary_data = _read_chk_section()
    section = transcoder.decode(chk_binary_data)
    assert len(section.entries) == 0


def test_it_decodes_and_encodes_without_changing_data():
    transcoder = ChkDd2Transcoder()
    chk_binary_data = _read_chk_section()
    section = transcoder.decode(chk_binary_data)
    actual_encoded_data = transcoder.encode(section, include_header=False)
    assert actual_encoded_data == chk_binary_data
    assert transcoder.decode(actual_encoded_data) == transcoder.decode(chk_binary_data)
