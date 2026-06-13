"""THG2 - Sprites.

This section contains sprite placement data.  Each entry is 10 bytes: u16 sprite_id, u16
x, u16 y, u8 owner, u8 unused, u16 flags.

The section may contain zero or more entries.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..decoded_chk_section import DecodedChkSection
from .decoded_thg2_entry import DecodedThg2Entry


@dataclasses.dataclass(frozen=True)
class DecodedThg2Section(DecodedChkSection):
    """Represent THG2 - Sprites section.

    :param _entries: tuple of decoded sprite entries
    """

    _entries: tuple[DecodedThg2Entry, ...]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.THG2

    @property
    def entries(self) -> tuple[DecodedThg2Entry, ...]:
        return self._entries
