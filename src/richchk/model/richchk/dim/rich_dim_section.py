"""DIM - Map Dimensions.

Required for all versions and all game types. Validation: Must be size of 4 bytes.

This section specifies the width and height of the map in tiles.

u16: Width of the map in tiles

u16: Height of the map in tiles
"""
import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection


@dataclasses.dataclass(frozen=True)
class RichDimSection(RichChkSection):

    _width: int
    _height: int

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.DIM

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height
