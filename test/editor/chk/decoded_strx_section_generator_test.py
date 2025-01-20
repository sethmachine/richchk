""""""

from richchk.editor.chk.decoded_strx_section_generator import (
    DecodedStrxSectionGenerator,
)
from richchk.model.chk.str.decoded_str_section import DecodedStrSection
from richchk.model.chk.strx.decoded_strx_section import DecodedStrxSection
from richchk.transcoder.chk.transcoders.chk_str_transcoder import ChkStrTranscoder
from richchk.transcoder.chk.transcoders.chk_strx_transcoder import ChkStrxTranscoder

from ...chk_resources import CHK_SECTION_FILE_PATHS
from .str_test_utils import assert_string_offsets_are_valid_for_strx

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


def test_it_generates_strx_from_str():
    str_transcoder = ChkStrTranscoder()
    strx_transcoder = ChkStrxTranscoder()
    str_section = str_transcoder.decode(_read_chk_section())
    strx_section = DecodedStrxSectionGenerator.generate_strx_from_str(str_section)
    strx_bytes = strx_transcoder.encode(strx_section, include_header=False)
    strx_again = strx_transcoder.decode(strx_bytes)
    assert strx_again == strx_section
    _assert_strx_equals_str(strx_section, str_section)
    _assert_strx_equals_str(strx_again, str_section)
    assert_string_offsets_are_valid_for_strx(strx_section)


def _assert_strx_equals_str(strx: DecodedStrxSection, str_: DecodedStrSection):
    assert strx.number_of_strings == str_.number_of_strings
    assert len(strx.strings_offsets) == len(str_.strings_offsets)
    assert strx.strings == str_.strings
