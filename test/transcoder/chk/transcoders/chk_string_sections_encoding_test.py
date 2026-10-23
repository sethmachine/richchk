import logging

import pytest

from richchk.model.chk.str.decoded_str_section import DecodedStrSection
from richchk.model.chk.strx.decoded_strx_section import DecodedStrxSection
from richchk.transcoder.chk.transcoders.chk_str_transcoder import ChkStrTranscoder
from richchk.transcoder.chk.transcoders.chk_strx_transcoder import ChkStrxTranscoder

from ..str_binary_builder import build_str_binary, build_strx_binary

_KOREAN = "가나다"
_KOREAN_CP949 = _KOREAN.encode("cp949")

_CASES = [
    pytest.param(ChkStrTranscoder, build_str_binary, DecodedStrSection, id="STR"),
    pytest.param(ChkStrxTranscoder, build_strx_binary, DecodedStrxSection, id="STRx"),
]


@pytest.mark.parametrize("transcoder_cls,build,section_cls", _CASES)
def test_ascii_strings_are_utf8(transcoder_cls, build, section_cls):
    section = transcoder_cls().decode(build([b"", b"hello"]))
    assert isinstance(section, section_cls)
    assert section.encoding == "utf-8"
    assert section.strings == ["", "hello"]


@pytest.mark.parametrize("transcoder_cls,build,section_cls", _CASES)
def test_utf8_strings_are_utf8(transcoder_cls, build, section_cls):
    data = build([b"", _KOREAN.encode("utf-8")])
    section = transcoder_cls().decode(data)
    assert section.encoding == "utf-8"
    assert section.strings == ["", _KOREAN]
    assert transcoder_cls().encode(section, include_header=False) == data


@pytest.mark.parametrize("transcoder_cls,build,section_cls", _CASES)
def test_non_utf8_strings_fall_back_to_cp1252_and_round_trip(
    transcoder_cls, build, section_cls
):
    data = build([b"", "café".encode("cp1252"), _KOREAN_CP949])
    section = transcoder_cls().decode(data)
    assert section.encoding == "cp1252"
    assert section.strings[1] == "café"
    assert transcoder_cls().encode(section, include_header=False) == data


@pytest.mark.parametrize("transcoder_cls,build,section_cls", _CASES)
def test_fallback_logs_a_warning_naming_the_encoding(
    transcoder_cls, build, section_cls
):
    messages = []

    class _Capture(logging.Handler):
        def emit(self, record):
            messages.append(record.getMessage())

    transcoder = transcoder_cls()
    handler = _Capture(level=logging.WARNING)
    transcoder._log.addHandler(handler)
    try:
        transcoder.decode(build([b"", _KOREAN_CP949]))
        transcoder.decode(build([b"", _KOREAN_CP949]), string_encoding="cp949")
    finally:
        transcoder._log.removeHandler(handler)
    assert len(messages) == 1
    assert "cp1252" in messages[0]


@pytest.mark.parametrize("transcoder_cls,build,section_cls", _CASES)
@pytest.mark.parametrize("requested", [None, "auto"])
def test_auto_matches_default(transcoder_cls, build, section_cls, requested):
    data = build([b"", _KOREAN_CP949])
    assert transcoder_cls().decode(data, string_encoding=requested) == (
        transcoder_cls().decode(data)
    )


@pytest.mark.parametrize("transcoder_cls,build,section_cls", _CASES)
def test_explicit_encoding_decodes_the_text_and_round_trips(
    transcoder_cls, build, section_cls
):
    data = build([b"", _KOREAN_CP949, b"ascii"])
    section = transcoder_cls().decode(data, string_encoding="cp949")
    assert section.encoding == "cp949"
    assert section.strings == ["", _KOREAN, "ascii"]
    assert transcoder_cls().encode(section, include_header=False) == data


@pytest.mark.parametrize("transcoder_cls,build,section_cls", _CASES)
def test_bytes_invalid_in_the_encoding_are_preserved(
    transcoder_cls, build, section_cls
):
    # a cp949 string, a UTF-8 string and a stray byte, all in one cp949 map
    raw = [b"", _KOREAN_CP949, "é".encode("utf-8"), b"x\xffy"]
    data = build(raw)
    section = transcoder_cls().decode(data, string_encoding="utf-8")
    assert section.strings[1] != _KOREAN
    assert section.strings[2] == "é"
    assert transcoder_cls().encode(section, include_header=False) == data
    section = transcoder_cls().decode(data, string_encoding="cp949")
    assert section.strings[1] == _KOREAN
    assert transcoder_cls().encode(section, include_header=False) == data


@pytest.mark.parametrize("transcoder_cls,build,section_cls", _CASES)
def test_section_default_encoding_is_utf8_for_existing_callers(
    transcoder_cls, build, section_cls
):
    section = section_cls(_number_of_strings=1, _string_offsets=[6], _strings=["é"])
    assert section.encoding == "utf-8"
    data = transcoder_cls().encode(section, include_header=False)
    assert data.endswith("é".encode("utf-8") + b"\0")
