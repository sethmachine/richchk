"""Decode and encode DD2 - Doodads.

Each entry is 8 bytes: u16 doodad_id, u16 x, u16 y, u8 owner, u8 enabled.
"""

import struct

from ....model.chk.dd2.decoded_dd2_entry import DecodedDd2Entry
from ....model.chk.dd2.decoded_dd2_section import DecodedDd2Section
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder

_DD2_ENTRY_STRUCT = struct.Struct("HHHBB")
_DD2_ENTRY_SIZE = _DD2_ENTRY_STRUCT.size


class ChkDd2Transcoder(
    ChkSectionTranscoder[DecodedDd2Section],
    _RegistrableTranscoder,
    chk_section_name=DecodedDd2Section.section_name(),
):
    def decode(self, chk_section_binary_data: bytes) -> DecodedDd2Section:
        if len(chk_section_binary_data) == 0:
            return DecodedDd2Section(_entries=())
        entries: list[DecodedDd2Entry] = []
        num_entries = len(chk_section_binary_data) // _DD2_ENTRY_SIZE
        offset = 0
        for _ in range(num_entries):
            doodad_id, x, y, owner, enabled = _DD2_ENTRY_STRUCT.unpack_from(
                chk_section_binary_data, offset
            )
            entries.append(
                DecodedDd2Entry(
                    _doodad_id=doodad_id,
                    _x=x,
                    _y=y,
                    _owner=owner,
                    _enabled=enabled,
                )
            )
            offset += _DD2_ENTRY_SIZE
        return DecodedDd2Section(_entries=tuple(entries))

    def _encode(self, decoded_chk_section: DecodedDd2Section) -> bytes:
        entries = decoded_chk_section.entries
        if len(entries) == 0:
            return b""
        buf = bytearray(len(entries) * _DD2_ENTRY_SIZE)
        offset = 0
        for entry in entries:
            _DD2_ENTRY_STRUCT.pack_into(
                buf,
                offset,
                entry.doodad_id,
                entry.x,
                entry.y,
                entry.owner,
                entry.enabled,
            )
            offset += _DD2_ENTRY_SIZE
        return bytes(buf)
