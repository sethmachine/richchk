import logging
import struct

import pytest

from richchk.io.chk.chk_io import ChkIo
from richchk.model.chk.unknown.decoded_unknown_section import DecodedUnknownSection
from richchk.model.chk.wav.decoded_wav_section import DecodedWavSection


def _chunk(name: bytes, data: bytes) -> bytes:
    assert len(name) == 4
    return name + struct.pack("I", len(data)) + data


def _valid_wav() -> bytes:
    return _chunk(b"WAV ", struct.pack("512I", *range(512)))


def _unknown(chk, name: bytes) -> list[DecodedUnknownSection]:
    return [
        s
        for s in chk.decoded_chk_sections
        if isinstance(s, DecodedUnknownSection) and s.actual_section_name_bytes == name
    ]


def test_it_keeps_a_wav_section_that_is_too_short_as_an_unknown_section(caplog):
    data = _valid_wav() + _chunk(b"WAV ", b"")
    with caplog.at_level(logging.ERROR):
        chk = ChkIo().decode_chk_binary_data(data)
    assert [type(s) for s in chk.decoded_chk_sections] == [
        DecodedWavSection,
        DecodedUnknownSection,
    ]
    assert _unknown(chk, b"WAV ")[0].chk_binary_data == b""
    messages = [r.getMessage() for r in caplog.records if "WAV " in r.getMessage()]
    assert any("Failed to decode CHK section" in m for m in messages)
    assert any("ignores invalid sections" in m for m in messages)


def test_it_writes_back_the_invalid_section_unchanged():
    data = _valid_wav() + _chunk(b"WAV ", b"ab") + _chunk(b"MTXM", b"abc")
    chk_io = ChkIo()
    assert chk_io.encode_chk_to_bytes(chk_io.decode_chk_binary_data(data)) == data


def test_it_exposes_a_readable_name_for_display_only():
    chk = ChkIo().decode_chk_binary_data(
        _chunk(b"TYPE", b"x") + _chunk(b"\xf8AB ", b"y")
    )
    unknown = [
        s for s in chk.decoded_chk_sections if isinstance(s, DecodedUnknownSection)
    ]
    assert [s.actual_section_name for s in unknown] == ["TYPE", "\\xf8AB "]
    assert [s.actual_section_name_bytes for s in unknown] == [b"TYPE", b"\xf8AB "]


def test_it_round_trips_a_section_name_with_bytes_above_ascii():
    data = _valid_wav() + _chunk(b"\xf8\x01\xff\x80", b"junk")
    chk_io = ChkIo()
    chk = chk_io.decode_chk_binary_data(data)
    assert _unknown(chk, b"\xf8\x01\xff\x80")[0].chk_binary_data == b"junk"
    assert chk_io.encode_chk_to_bytes(chk) == data


def test_it_ignores_trailing_bytes_too_short_for_a_header_and_logs_an_error(caplog):
    valid = _valid_wav()
    for trailing in (b"\x00", b"abc", b"abcd", b"abcd\x01\x00\x00"):
        with caplog.at_level(logging.ERROR):
            chk = ChkIo().decode_chk_binary_data(valid + trailing)
        assert [type(s) for s in chk.decoded_chk_sections] == [DecodedWavSection]
        assert ChkIo().encode_chk_to_bytes(chk) == valid
    assert any("trailing bytes" in r.getMessage() for r in caplog.records)


def test_it_does_not_hide_a_broken_string_section():
    data = _valid_wav() + _chunk(b"STR ", b"\x05\x00")
    with pytest.raises(Exception):
        ChkIo().decode_chk_binary_data(data)


def test_it_still_decodes_valid_sections_without_logging_errors(caplog):
    with caplog.at_level(logging.ERROR):
        chk = ChkIo().decode_chk_binary_data(_valid_wav())
    assert [type(s) for s in chk.decoded_chk_sections] == [DecodedWavSection]
    assert not [r for r in caplog.records if "Failed to decode" in r.getMessage()]
