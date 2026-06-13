"""DD2 - Doodads.

This section contains doodad placement data.  Each entry is 8 bytes: u16 doodad_id, u16
x, u16 y, u8 owner, u8 enabled.

The section may contain zero or more entries.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..decoded_chk_section import DecodedChkSection
from .decoded_dd2_entry import DecodedDd2Entry


@dataclasses.dataclass(frozen=True)
class DecodedDd2Section(DecodedChkSection):
    """Represent DD2 - Doodads section.

    :param _entries: tuple of decoded doodad entries
    """

    _entries: tuple[DecodedDd2Entry, ...]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.DD2

    @property
    def entries(self) -> tuple[DecodedDd2Entry, ...]:
        return self._entries
