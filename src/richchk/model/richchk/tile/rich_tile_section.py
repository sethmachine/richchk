"""TILE - Terrain (legacy).

Not required.

This section contains the terrain data for the map. It is a flat array of u16 tile
values. The number of entries is width * height (from the DIM section). StarCraft
typically uses MTXM instead of TILE for terrain data, but TILE may be present in older
maps.

u16[width * height]: Tile values
"""
from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING

from ...chk_section_name import ChkSectionName
from ..mtxm.rich_tile import RichTile
from ..rich_chk_section import RichChkSection

if TYPE_CHECKING:
    from ..mtxm.rich_mtxm_section import RichMtxmSection


@dataclasses.dataclass(frozen=True)
class RichTileSection(RichChkSection):

    _tiles: list[RichTile]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.TILE

    @property
    def tiles(self) -> list[RichTile]:
        return self._tiles

    @classmethod
    def from_mtxm(cls, mtxm: "RichMtxmSection") -> "RichTileSection":
        return cls(_tiles=mtxm.tiles)
