"""SIDE - Player Races.

Not required. Validation: Must be size of 12 bytes.

u8[12]: One byte per player slot (0-11) designating the player's race.

0x00 - Zerg
0x01 - Terran
0x02 - Protoss
0x03 - Invalid (Independent)
0x04 - Invalid (Neutral)
0x05 - User Select
0x06 - Random (Forced)
0x07 - Inactive
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..decoded_chk_section import DecodedChkSection

_NUM_PLAYERS = 12


@dataclasses.dataclass(frozen=True)
class DecodedSideSection(DecodedChkSection):
    """Represent SIDE - Player Races.

    :param _player_races: u8[12] one byte per player slot indicating the player's race
    """

    _player_races: list[int]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.SIDE

    @property
    def player_races(self) -> list[int]:
        return self._player_races
