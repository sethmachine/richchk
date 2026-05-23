"""SIDE - Player Races.

Not required. Validation: Must be size of 12 bytes.

u8[12]: One byte per player slot (0-11) designating the player's race.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection
from .player_race import PlayerRace


@dataclasses.dataclass(frozen=True)
class RichSideSection(RichChkSection):
    """Represent SIDE - Player Races.

    :param _player_races: list of PlayerRace, one per player slot (12 total)
    """

    _player_races: list[PlayerRace]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.SIDE

    @property
    def player_races(self) -> list[PlayerRace]:
        return self._player_races
