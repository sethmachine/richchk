"""TILE - Terrain (legacy).

Not required.

This section contains the "pure" terrain tile data derived from ISOM, without doodad
overlays. The number of entries is width * height (from the DIM section). StarCraft
reads MTXM (which includes doodad tiles) at runtime; TILE exists for StarEdit's internal
use.

u16[width * height]: Tile values
"""
import dataclasses

from ...chk_section_name import ChkSectionName
from ..mtxm.rich_tile import RichTile
from ..rich_chk_section import RichChkSection


@dataclasses.dataclass(frozen=True)
class RichTileSection(RichChkSection):

    _tiles: list[RichTile]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.TILE

    @property
    def tiles(self) -> list[RichTile]:
        return self._tiles
