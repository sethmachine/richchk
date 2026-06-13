"""THG2 - Sprites.

Rich representation of the THG2 section containing sprite placement data.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection
from .rich_thg2_entry import RichSprite


@dataclasses.dataclass(frozen=True)
class RichThg2Section(RichChkSection):
    """Represent THG2 - Sprites section.

    :param _sprites: list of sprites placed on the map
    """

    _sprites: list[RichSprite]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.THG2

    @property
    def sprites(self) -> list[RichSprite]:
        return self._sprites
