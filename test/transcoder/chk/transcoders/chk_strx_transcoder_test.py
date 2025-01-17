from richchk.model.chk.strx.decoded_strx_section import DecodedStrxSection
from richchk.transcoder.chk.transcoders.chk_strx_transcoder import ChkStrxTranscoder

from ....chk_resources import CHK_SECTION_FILE_PATHS

# these strings were added into the CHK section by using a GUI map editor
_EXPECTED_STRINGS = [
    "test-string-1-marine",
    "test-string-2-firebat",
    "test-string-3-ghost",
]


def _read_chk_section() -> bytes:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedStrxSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return chk_binary_data


def test_it_decodes_str_chk_section_with_expected_strings():
    transcoder = ChkStrxTranscoder()
    chk_binary_data = _read_chk_section()
    strx_section = transcoder.decode(chk_binary_data)
    assert set(_EXPECTED_STRINGS).issubset(set(strx_section.strings))


def test_it_decodes_and_encodes_without_changing_data():
    transcoder = ChkStrxTranscoder()
    chk_binary_data = _read_chk_section()
    strx_section = transcoder.decode(chk_binary_data)
    actual_encoded_data = transcoder.encode(strx_section, include_header=False)
    assert actual_encoded_data == chk_binary_data
    assert transcoder.decode(actual_encoded_data) == transcoder.decode(chk_binary_data)
