import struct

import pytest

from richchk.io.chk.chk_io import ChkIo
from richchk.model.chk_section_name import ChkSectionName

from ...transcoder.chk.str_binary_builder import build_str_binary, build_strx_binary

_KOREAN = "가나다"
_RAW_STRINGS = [b"", _KOREAN.encode("cp949"), b"ascii"]


def _chunk(name: bytes, data: bytes) -> bytes:
    return name + struct.pack("<I", len(data)) + data


def _chk_with_str() -> bytes:
    return _chunk(b"STR ", build_str_binary(_RAW_STRINGS))


def _only_section(chk, name: ChkSectionName):
    sections = chk.get_sections_by_name(name)
    assert len(sections) == 1
    return sections[0]


def test_decode_binary_data_detects_the_encoding_by_default():
    section = _only_section(
        ChkIo().decode_chk_binary_data(_chk_with_str()), ChkSectionName.STR
    )
    assert section.encoding == "cp1252"


def test_decode_binary_data_with_explicit_encoding():
    data = _chk_with_str()
    chk = ChkIo().decode_chk_binary_data(data, string_encoding="cp949")
    section = _only_section(chk, ChkSectionName.STR)
    assert section.encoding == "cp949"
    assert section.strings == ["", _KOREAN, "ascii"]
    # writing it back does not change any bytes
    assert ChkIo().encode_chk_to_bytes(chk) == data


def test_decode_file_with_explicit_encoding(tmp_path):
    path = tmp_path / "scenario.chk"
    path.write_bytes(_chk_with_str())
    section = _only_section(
        ChkIo().decode_chk_file(str(path), string_encoding="cp949"),
        ChkSectionName.STR,
    )
    assert section.strings == ["", _KOREAN, "ascii"]


def test_decode_strx_with_explicit_encoding():
    data = _chunk(b"STRx", build_strx_binary(_RAW_STRINGS))
    chk = ChkIo().decode_chk_binary_data(data, string_encoding="cp949")
    section = _only_section(chk, ChkSectionName.STRX)
    assert section.encoding == "cp949"
    assert section.strings == ["", _KOREAN, "ascii"]
    assert ChkIo().encode_chk_to_bytes(chk) == data


def test_other_sections_are_not_affected_by_the_encoding():
    # 64 bytes of UPUS (CUWP slots used) is a section without any text
    upus = _chunk(b"UPUS", bytes(range(64)))
    chk_default = ChkIo().decode_chk_binary_data(upus + _chk_with_str())
    chk_cp949 = ChkIo().decode_chk_binary_data(
        upus + _chk_with_str(), string_encoding="cp949"
    )
    assert chk_default.get_sections_by_name(
        ChkSectionName.UPUS
    ) == chk_cp949.get_sections_by_name(ChkSectionName.UPUS)


@pytest.mark.parametrize("bad", ["not-a-codec", "utf-16"])
def test_invalid_encoding_is_rejected_before_reading(bad, tmp_path):
    with pytest.raises(ValueError):
        ChkIo().decode_chk_binary_data(_chk_with_str(), string_encoding=bad)
    with pytest.raises(ValueError):
        ChkIo().decode_chk_file(str(tmp_path / "missing.chk"), string_encoding=bad)
