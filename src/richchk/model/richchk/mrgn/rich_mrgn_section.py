"""MRGN - Locations."""
import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection
from .rich_location import RichLocation


@dataclasses.dataclass(frozen=True)
class RichMrgnSection(RichChkSection):

    _locations: list[RichLocation]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.MRGN

    @property
    def locations(self) -> list[RichLocation]:
        return self._locations
