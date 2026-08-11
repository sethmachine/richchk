"""MBRF - Mission Briefings.

This section contains all of the mission briefings shown to players before the map
starts. It uses exactly the same format as the TRIG section, with the distinction that
all 16 condition slots are null except the very first one, which only has a condition
byte of 13 to designate it as a mission briefing.

Validation: Must be a multiple of 2400 bytes. This section can be split; additional MBRF
sections will add more briefings.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..decoded_chk_section import DecodedChkSection
from ..trig.decoded_trigger import DecodedTrigger


@dataclasses.dataclass(frozen=True)
class DecodedMbrfSection(DecodedChkSection):
    """Represent MBRF section for all mission briefing data.

    :param _triggers: contains all the briefings in this MBRF section. Each briefing
        uses the same 2400-byte trigger structure as the TRIG section.
    """

    _triggers: list[DecodedTrigger]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.MBRF

    @property
    def triggers(self) -> list[DecodedTrigger]:
        return self._triggers
