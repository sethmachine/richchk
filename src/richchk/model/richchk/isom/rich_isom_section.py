"""ISOM - Isometric Terrain.

Rich representation of the ISOM section.  This is a simple pass-through of the raw u16
data for round-tripping without semantic interpretation.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection


@dataclasses.dataclass(frozen=True)
class RichIsomSection(RichChkSection):
    """Represent ISOM - Isometric Terrain.

    :param _data: flat array of u16 isometric terrain values
    """

    _data: list[int]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.ISOM

    @property
    def data(self) -> list[int]:
        return self._data
