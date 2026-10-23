import pytest

from richchk.editor.chk.decoded_str_section_editor import DecodedStrSectionEditor
from richchk.editor.chk.decoded_strx_section_editor import DecodedStrxSectionEditor
from richchk.editor.chk.decoded_strx_section_generator import (
    DecodedStrxSectionGenerator,
)
from richchk.io.richchk.rich_str_lookup_builder import RichStrLookupBuilder
from richchk.transcoder.chk.transcoders.chk_str_transcoder import ChkStrTranscoder
from richchk.transcoder.chk.transcoders.chk_strx_transcoder import ChkStrxTranscoder

from ...transcoder.chk.str_binary_builder import build_str_binary, build_strx_binary

_KOREAN = "가나다"
_NEW_KOREAN = "새글"
_RAW_STRINGS = [b"", _KOREAN.encode("cp949"), b"ascii", b"stray \xff byte"]
_EXPECTED_STRINGS = ["", _KOREAN, "ascii", "stray \udcff byte"]

_CASES = [
    pytest.param(ChkStrTranscoder, build_str_binary, DecodedStrSectionEditor, id="STR"),
    pytest.param(
        ChkStrxTranscoder, build_strx_binary, DecodedStrxSectionEditor, id="STRx"
    ),
]


def _add(editor, strings, section):
    if isinstance(editor, DecodedStrSectionEditor):
        return editor.add_strings_to_str_section(strings, section)
    return editor.add_strings_to_strx_section(strings, section)


@pytest.mark.parametrize("transcoder_cls,build,editor_cls", _CASES)
def test_adding_strings_keeps_the_encoding_and_every_existing_byte(
    transcoder_cls, build, editor_cls
):
    original_data = build(_RAW_STRINGS)
    section = transcoder_cls().decode(original_data, string_encoding="cp949")
    new_section = _add(editor_cls(), [_NEW_KOREAN, "more"], section)
    assert new_section.encoding == "cp949"
    assert new_section.strings == section.strings + [_NEW_KOREAN, "more"]
    new_data = transcoder_cls().encode(new_section, include_header=False)
    # the new section decodes back to the same text, with the same encoding
    redecoded = transcoder_cls().decode(new_data, string_encoding="cp949")
    assert redecoded == new_section
    # offsets are in bytes of the section's encoding: each string is found by its ID
    lookup = RichStrLookupBuilder().build_lookup(new_section)
    found = [
        lookup.get_string_by_id(i + 1).value
        for i in range(new_section.number_of_strings)
    ]
    assert found == _EXPECTED_STRINGS + [_NEW_KOREAN, "more"]
    # the original strings are byte-for-byte unchanged
    for raw in _RAW_STRINGS:
        assert raw + b"\0" in new_data


@pytest.mark.parametrize("transcoder_cls,build,editor_cls", _CASES)
def test_new_string_offsets_use_the_byte_length_in_the_encoding(
    transcoder_cls, build, editor_cls
):
    # Korean text is 2 bytes per character in cp949 but 3 in UTF-8, so the offset of
    # the second added string depends on the encoding
    section = transcoder_cls().decode(build(_RAW_STRINGS), string_encoding="cp949")
    new_section = _add(editor_cls(), [_NEW_KOREAN, "more"], section)
    offsets = new_section.strings_offsets
    assert offsets[-1] - offsets[-2] == len(_NEW_KOREAN.encode("cp949")) + 1


@pytest.mark.parametrize("transcoder_cls,build,editor_cls", _CASES)
def test_adding_a_string_the_encoding_cannot_represent_fails_to_encode(
    transcoder_cls, build, editor_cls
):
    section = transcoder_cls().decode(build(_RAW_STRINGS), string_encoding="cp949")
    new_section = _add(editor_cls(), ["\U0001f600"], section)
    with pytest.raises(UnicodeEncodeError):
        transcoder_cls().encode(new_section, include_header=False)


@pytest.mark.parametrize("transcoder_cls,build,editor_cls", _CASES)
def test_adding_no_new_strings_returns_the_same_section(
    transcoder_cls, build, editor_cls
):
    section = transcoder_cls().decode(build(_RAW_STRINGS), string_encoding="cp949")
    assert _add(editor_cls(), [_KOREAN], section) is section


def test_generating_strx_from_str_keeps_the_encoding_and_bytes():
    str_section = ChkStrTranscoder().decode(
        build_str_binary(_RAW_STRINGS), string_encoding="cp949"
    )
    strx_section = DecodedStrxSectionGenerator.generate_strx_from_str(str_section)
    assert strx_section.encoding == "cp949"
    lookup = RichStrLookupBuilder().build_lookup(strx_section)
    found = [
        lookup.get_string_by_id(i + 1).value
        for i in range(strx_section.number_of_strings)
    ]
    assert found == _EXPECTED_STRINGS
    data = ChkStrxTranscoder().encode(strx_section, include_header=False)
    for raw in _RAW_STRINGS:
        assert raw + b"\0" in data


def test_lookup_builder_uses_the_section_encoding():
    data = build_str_binary(_RAW_STRINGS)
    cp949 = ChkStrTranscoder().decode(data, string_encoding="cp949")
    assert RichStrLookupBuilder().build_lookup(cp949).get_string_by_id(2).value == (
        _KOREAN
    )
    auto = ChkStrTranscoder().decode(data)
    assert auto.encoding == "cp1252"
    assert RichStrLookupBuilder().build_lookup(auto).get_string_by_id(2).value != (
        _KOREAN
    )
