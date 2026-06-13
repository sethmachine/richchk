"""ISOM - Isometric Terrain.

This section contains isometric terrain data stored as a flat array of u16 values.  The
total number of values is ((width/2 + 1) * (height + 1)) * 4.

This section is modeled as raw data for round-tripping without semantic interpretation.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..decoded_chk_section import DecodedChkSection


@dataclasses.dataclass(frozen=True)
class DecodedIsomSection(DecodedChkSection):
    """Represent ISOM - Isometric Terrain.

    :param _data: flat array of u16 isometric terrain values
    """

    _data: tuple[int, ...]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.ISOM

    @property
    def data(self) -> tuple[int, ...]:
        return self._data
