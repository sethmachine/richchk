"""TILE - Terrain (legacy).

Not required.

This section contains the terrain data for the map. It is a flat array of u16 tile
values. The number of entries is width * height (from the DIM section). StarCraft
typically uses MTXM instead of TILE for terrain data, but TILE may be present in older
maps.

u16[width * height]: Tile values
"""

import dataclasses
from typing import Tuple

from ...chk_section_name import ChkSectionName
from ..decoded_chk_section import DecodedChkSection


@dataclasses.dataclass(frozen=True)
class DecodedTileSection(DecodedChkSection):
    """Represent TILE - Terrain (legacy).

    :param _tiles: flat array of u16 tile values
    """

    _tiles: Tuple[int, ...]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.TILE

    @property
    def tiles(self) -> Tuple[int, ...]:
        return self._tiles
