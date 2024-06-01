from richchk.model.chk.str.decoded_str_section import DecodedStrSection
from richchk.transcoder.chk.transcoders.chk_str_transcoder import ChkStrTranscoder

from ....chk_resources import CHK_SECTION_FILE_PATHS

# these strings were added into the CHK section by using a GUI map editor
_EXPECTED_STRINGS = [
    "test-string-1-marine",
    "test-string-2-firebat",
    "test-string-3-ghost",
]


def _read_chk_section() -> bytes:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedStrSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return chk_binary_data


def test_it_decodes_str_chk_section_with_expected_strings():
    transcoder: ChkStrTranscoder = ChkStrTranscoder()
    chk_binary_data = _read_chk_section()
    str_section: DecodedStrSection = transcoder.decode(chk_binary_data)
    assert set(_EXPECTED_STRINGS).issubset(set(str_section.strings))


def test_it_decodes_and_encodes_without_changing_data():
    transcoder: ChkStrTranscoder = ChkStrTranscoder()
    chk_binary_data = _read_chk_section()
    str_section: DecodedStrSection = transcoder.decode(chk_binary_data)
    actual_encoded_data = transcoder.encode(str_section, include_header=False)
    assert actual_encoded_data == chk_binary_data
    assert transcoder.decode(actual_encoded_data) == transcoder.decode(chk_binary_data)
