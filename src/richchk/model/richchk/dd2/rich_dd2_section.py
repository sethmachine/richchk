"""DD2 - Doodads.

Rich representation of the DD2 section containing doodad placement data.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection
from .rich_dd2_entry import RichDd2Entry


@dataclasses.dataclass(frozen=True)
class RichDd2Section(RichChkSection):
    """Represent DD2 - Doodads section.

    :param _entries: tuple of rich doodad entries
    """

    _entries: tuple[RichDd2Entry, ...]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.DD2

    @property
    def entries(self) -> tuple[RichDd2Entry, ...]:
        return self._entries
