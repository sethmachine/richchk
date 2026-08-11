"""MBRF - Mission Briefings.

This section contains all of the mission briefings shown to players. It uses the same
binary format as the TRIG section (2400 bytes per entry), but with a restricted set of
actions (IDs 0-9) and a fixed marker in the first condition slot.

This section can be split; additional MBRF sections will add more briefings.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection
from .rich_briefing import RichBriefing


@dataclasses.dataclass(frozen=True)
class RichMbrfSection(RichChkSection):
    """Represent MBRF section for all mission briefing data."""

    _briefings: list[RichBriefing]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.MBRF

    @property
    def briefings(self) -> list[RichBriefing]:
        return self._briefings
