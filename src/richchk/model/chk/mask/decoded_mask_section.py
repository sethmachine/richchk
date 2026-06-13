"""MASK - Fog of War.

This section contains fog of war data for each map tile.  One byte per tile, stored as a
flat array of u8 values in row-major order (width * height bytes).
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..decoded_chk_section import DecodedChkSection


@dataclasses.dataclass(frozen=True)
class DecodedMaskSection(DecodedChkSection):
    """Represent MASK - Fog of War.

    :param _fog_data: flat array of u8 fog values, one per map tile
    """

    _fog_data: tuple[int, ...]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.MASK

    @property
    def fog_data(self) -> tuple[int, ...]:
        return self._fog_data
