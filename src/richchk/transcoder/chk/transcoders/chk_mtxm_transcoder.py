"""Decode and encode MTXM - Terrain.

Required for all versions and all game types.

This section contains the terrain data for the map. It is a flat array of u16 tile
values, where each value represents a megatile index. The number of entries is width *
height (from the DIM section).

u16[width * height]: Tile values
"""

import struct

from ....model.chk.mtxm.decoded_mtxm_section import DecodedMtxmSection
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder


class ChkMtxmTranscoder(
    ChkSectionTranscoder[DecodedMtxmSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedMtxmSection.section_name(),
):
    def decode(self, chk_section_binary_data: bytes) -> DecodedMtxmSection:
        num_tiles = len(chk_section_binary_data) // 2
        tiles = struct.unpack("<{}H".format(num_tiles), chk_section_binary_data)
        return DecodedMtxmSection(_tiles=tiles)

    def _encode(self, decoded_chk_section: DecodedMtxmSection) -> bytes:
        num_tiles = len(decoded_chk_section.tiles)
        return struct.pack("<{}H".format(num_tiles), *decoded_chk_section.tiles)
