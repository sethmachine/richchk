"""DD2 - Doodads.

Rich representation of the DD2 section containing doodad placement data.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection
from .rich_dd2_entry import RichDoodad


@dataclasses.dataclass(frozen=True)
class RichDd2Section(RichChkSection):
    """Represent DD2 - Doodads section.

    :param _doodads: list of doodads placed on the map
    """

    _doodads: list[RichDoodad]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.DD2

    @property
    def doodads(self) -> list[RichDoodad]:
        return self._doodads
