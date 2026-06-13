"""THG2 - Sprites.

Rich representation of the THG2 section containing sprite placement data.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection
from .rich_thg2_entry import RichThg2Entry


@dataclasses.dataclass(frozen=True)
class RichThg2Section(RichChkSection):
    """Represent THG2 - Sprites section.

    :param _entries: tuple of rich sprite entries
    """

    _entries: tuple[RichThg2Entry, ...]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.THG2

    @property
    def entries(self) -> tuple[RichThg2Entry, ...]:
        return self._entries
