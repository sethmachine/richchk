"""MTXM - Terrain.

Required for all versions and all game types.

This section contains the terrain data for the map. It is a flat array of u16 tile
values, where each value represents a megatile index. The number of entries is width *
height (from the DIM section).

u16[width * height]: Tile values
"""
import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection
from .rich_tile import RichTile


@dataclasses.dataclass(frozen=True)
class RichMtxmSection(RichChkSection):

    _tiles: list[RichTile]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.MTXM

    @property
    def tiles(self) -> list[RichTile]:
        return self._tiles
