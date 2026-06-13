"""Decode and encode THG2 - Sprites.

Each entry is 10 bytes: u16 sprite_id, u16 x, u16 y, u8 owner, u8 unused, u16 flags.
"""

import struct

from ....model.chk.thg2.decoded_thg2_entry import DecodedThg2Entry
from ....model.chk.thg2.decoded_thg2_section import DecodedThg2Section
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder

_THG2_ENTRY_STRUCT = struct.Struct("HHHBBH")
_THG2_ENTRY_SIZE = _THG2_ENTRY_STRUCT.size


class ChkThg2Transcoder(
    ChkSectionTranscoder[DecodedThg2Section],
    _RegistrableTranscoder,
    chk_section_name=DecodedThg2Section.section_name(),
):
    def decode(self, chk_section_binary_data: bytes) -> DecodedThg2Section:
        if len(chk_section_binary_data) == 0:
            return DecodedThg2Section(_entries=())
        entries: list[DecodedThg2Entry] = []
        num_entries = len(chk_section_binary_data) // _THG2_ENTRY_SIZE
        offset = 0
        for _ in range(num_entries):
            sprite_id, x, y, owner, unused, flags = _THG2_ENTRY_STRUCT.unpack_from(
                chk_section_binary_data, offset
            )
            entries.append(
                DecodedThg2Entry(
                    _sprite_id=sprite_id,
                    _x=x,
                    _y=y,
                    _owner=owner,
                    _unused=unused,
                    _flags=flags,
                )
            )
            offset += _THG2_ENTRY_SIZE
        return DecodedThg2Section(_entries=tuple(entries))

    def _encode(self, decoded_chk_section: DecodedThg2Section) -> bytes:
        entries = decoded_chk_section.entries
        if len(entries) == 0:
            return b""
        buf = bytearray(len(entries) * _THG2_ENTRY_SIZE)
        offset = 0
        for entry in entries:
            _THG2_ENTRY_STRUCT.pack_into(
                buf,
                offset,
                entry.sprite_id,
                entry.x,
                entry.y,
                entry.owner,
                entry.unused,
                entry.flags,
            )
            offset += _THG2_ENTRY_SIZE
        return bytes(buf)
