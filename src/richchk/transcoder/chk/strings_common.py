"""Maintain constants and helpers used for working with Strings throughout Starcraft CHK
format.

The CHK format does not record the encoding of the STR/STRx text.  Common encodings are
CP-1252, CP-949, and (Remastered) UTF-8, but anything is possible.  Strings are decoded
and encoded with the "surrogateescape" error handler: any byte that is not valid in the
chosen encoding is kept as a lone surrogate (U+DC80 to U+DCFF) and turned back into the
exact same byte when encoding.  This makes reading and writing lossless whatever the
actual encoding of the map is.
"""
import codecs
from typing import Iterable, Optional

_NULL_TERMINATE_CHAR_FOR_STRING: str = "\x00"
# encoding used for text that is always ASCII, e.g. AI script names and section names
_STRING_ENCODING: str = "utf-8"
# the encoding used for map strings when they are valid UTF-8 (including pure ASCII)
_DEFAULT_MAP_STRING_ENCODING: str = "utf-8"
# the encoding assumed for map strings that are not valid UTF-8.  This is the Western
# ANSI code page of Starcraft 1.16.  Other languages must be given explicitly.
_FALLBACK_MAP_STRING_ENCODING: str = "cp1252"
_STRING_ERROR_HANDLER: str = "surrogateescape"
AUTO_STRING_ENCODING: str = "auto"


def decode_string(raw_string: bytes, encoding: str) -> str:
    """Decode bytes from a string section, never raising on invalid bytes."""
    return raw_string.decode(encoding, _STRING_ERROR_HANDLER)


def encode_string(string: str, encoding: str) -> bytes:
    """Encode a string from a string section, restoring any escaped bytes."""
    return string.encode(encoding, _STRING_ERROR_HANDLER)


def detect_string_encoding(raw_strings: Iterable[bytes]) -> str:
    """Pick the encoding for all the strings of one map.

    The encoding is not stored in the CHK, and only UTF-8 can be reliably detected: it
    has a strict structure, whereas single byte encodings accept any bytes and the CJK
    encodings overlap.  So if every string is valid UTF-8 (this includes ASCII) the map
    is UTF-8, otherwise the Western fallback is assumed.
    """
    try:
        # NUL is valid UTF-8 and never part of a multi byte sequence, so decoding the
        # joined strings is the same as decoding each one.
        b"\0".join(raw_strings).decode("utf-8")
    except UnicodeDecodeError:
        return _FALLBACK_MAP_STRING_ENCODING
    return _DEFAULT_MAP_STRING_ENCODING


def resolve_string_encoding(
    string_encoding: Optional[str], raw_strings: Iterable[bytes]
) -> str:
    """Use the requested encoding, or detect it if None or "auto"."""
    if string_encoding is None or string_encoding == AUTO_STRING_ENCODING:
        return detect_string_encoding(raw_strings)
    return string_encoding


def validate_string_encoding(string_encoding: Optional[str]) -> Optional[str]:
    """Check an encoding requested by a caller, returning its canonical name.

    None and "auto" mean detect the encoding and are returned as None.  The encoding
    must be known to Python and must encode ASCII (and the NUL terminator) as plain
    bytes, since strings are split apart on NUL bytes.
    """
    if string_encoding is None or string_encoding == AUTO_STRING_ENCODING:
        return None
    try:
        name = codecs.lookup(string_encoding).name
    except LookupError as err:
        raise ValueError(f"Unknown string encoding: {string_encoding!r}") from err
    try:
        ascii_compatible = "a\0".encode(name) == b"a\0"
    except (UnicodeEncodeError, LookupError):
        ascii_compatible = False
    if not ascii_compatible:
        raise ValueError(
            f"String encoding {string_encoding!r} is not ASCII compatible, so it cannot "
            f"be used for CHK strings, which are NUL terminated."
        )
    return name
