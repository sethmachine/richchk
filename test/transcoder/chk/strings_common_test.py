import pytest

from richchk.transcoder.chk.strings_common import (
    decode_string,
    detect_string_encoding,
    encode_string,
    resolve_string_encoding,
    validate_string_encoding,
)

_KOREAN_CP949 = "가나다".encode("cp949")


def test_detect_is_utf8_for_no_strings():
    assert detect_string_encoding([]) == "utf-8"


def test_detect_is_utf8_for_ascii():
    assert detect_string_encoding([b"", b"hello", b"\x1eD\x1cragon"]) == "utf-8"


def test_detect_is_utf8_for_valid_non_ascii_utf8():
    assert detect_string_encoding([b"hello", "café".encode("utf-8")]) == "utf-8"


def test_detect_falls_back_to_cp1252_for_cp1252_text():
    assert detect_string_encoding([b"hello", "café".encode("cp1252")]) == "cp1252"


def test_detect_falls_back_to_cp1252_for_cjk_text():
    assert detect_string_encoding([_KOREAN_CP949]) == "cp1252"


def test_detect_falls_back_if_any_string_is_not_utf8():
    mixed = ["café".encode("utf-8"), "café".encode("cp1252")]
    assert detect_string_encoding(mixed) == "cp1252"


def test_detect_does_not_join_an_incomplete_sequence_into_the_next_string():
    # a truncated 2 byte UTF-8 sequence followed by another string is still invalid
    assert detect_string_encoding([b"\xc3", b"\xa9"]) == "cp1252"


@pytest.mark.parametrize("requested", [None, "auto"])
def test_resolve_detects_when_not_given(requested):
    assert resolve_string_encoding(requested, [_KOREAN_CP949]) == "cp1252"
    assert resolve_string_encoding(requested, [b"abc"]) == "utf-8"


def test_resolve_uses_the_requested_encoding():
    assert resolve_string_encoding("cp949", [b"abc"]) == "cp949"


@pytest.mark.parametrize(
    "raw,encoding",
    [
        (b"plain", "utf-8"),
        (b"caf\xe9", "utf-8"),  # invalid UTF-8
        (b"\x81\x8d\x8f\x90\x9d", "cp1252"),  # undefined in cp1252
        (_KOREAN_CP949 + b"\xff", "cp949"),  # valid cp949 then an invalid byte
        (b"\xe2\x82", "utf-8"),  # truncated sequence
        (bytes(range(1, 256)), "utf-8"),
        (bytes(range(1, 256)), "cp949"),
        (bytes(range(1, 256)), "shift_jis"),
        (bytes(range(1, 256)), "cp1252"),
    ],
)
def test_decode_then_encode_is_lossless_for_any_bytes(raw, encoding):
    assert encode_string(decode_string(raw, encoding), encoding) == raw


def test_decode_uses_the_encoding():
    assert decode_string(_KOREAN_CP949, "cp949") == "가나다"
    assert decode_string(_KOREAN_CP949, "cp1252") != "가나다"


@pytest.mark.parametrize(
    "requested,expected",
    [
        (None, None),
        ("auto", None),
        ("utf-8", "utf-8"),
        ("UTF8", "utf-8"),
        ("cp949", "cp949"),
        ("shift_jis", "shift_jis"),
        ("gbk", "gbk"),
        ("big5", "big5"),
    ],
)
def test_validate_string_encoding(requested, expected):
    assert validate_string_encoding(requested) == expected


def test_validate_rejects_unknown_encoding():
    with pytest.raises(ValueError, match="Unknown string encoding"):
        validate_string_encoding("not-a-codec")


@pytest.mark.parametrize("requested", ["utf-16", "utf-16-le", "utf-32"])
def test_validate_rejects_encodings_that_are_not_ascii_compatible(requested):
    with pytest.raises(ValueError, match="not ASCII compatible"):
        validate_string_encoding(requested)
