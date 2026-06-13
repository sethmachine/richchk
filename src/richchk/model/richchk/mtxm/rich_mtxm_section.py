"""MTXM - Terrain.

Required for all versions and all game types.

This section contains the terrain data for the map. It is a flat array of u16 tile
values, where each value represents a megatile index. The number of entries is width *
height (from the DIM section).

u16[width * height]: Tile values
"""
import dataclasses
from typing import Tuple

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection


@dataclasses.dataclass(frozen=True)
class RichMtxmSection(RichChkSection):

    _tiles: Tuple[int, ...]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.MTXM

    @property
    def tiles(self) -> Tuple[int, ...]:
        return self._tiles
