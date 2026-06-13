"""Decode and encode TILE - Terrain (legacy).

Not required.

This section contains the terrain data for the map. It is a flat array of u16 tile
values. The number of entries is width * height (from the DIM section). StarCraft
typically uses MTXM instead of TILE for terrain data, but TILE may be present in older
maps.

u16[width * height]: Tile values
"""

import struct

from ....model.chk.tile.decoded_tile_section import DecodedTileSection
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder


class ChkTileTranscoder(
    ChkSectionTranscoder[DecodedTileSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedTileSection.section_name(),
):
    def decode(self, chk_section_binary_data: bytes) -> DecodedTileSection:
        num_tiles = len(chk_section_binary_data) // 2
        tiles = struct.unpack("<{}H".format(num_tiles), chk_section_binary_data)
        return DecodedTileSection(_tiles=tiles)

    def _encode(self, decoded_chk_section: DecodedTileSection) -> bytes:
        num_tiles = len(decoded_chk_section.tiles)
        return struct.pack("<{}H".format(num_tiles), *decoded_chk_section.tiles)
