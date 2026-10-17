"""Build STR / STRx section binary data from raw byte strings, for tests."""
import struct


def build_str_binary(raw_strings: list[bytes]) -> bytes:
    """u16 count, u16 offsets (from section start), then NUL terminated strings."""
    return _build(raw_strings, "H", 2)


def build_strx_binary(raw_strings: list[bytes]) -> bytes:
    """u32 count, u32 offsets (from section start), then NUL terminated strings."""
    return _build(raw_strings, "I", 4)


def _build(raw_strings: list[bytes], fmt: str, width: int) -> bytes:
    offsets = []
    offset = width + width * len(raw_strings)
    for raw in raw_strings:
        offsets.append(offset)
        offset += len(raw) + 1
    header = struct.pack(f"<{fmt}", len(raw_strings))
    header += struct.pack(f"<{len(raw_strings)}{fmt}", *offsets)
    return header + b"".join(raw + b"\0" for raw in raw_strings)
