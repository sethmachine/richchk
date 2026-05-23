"""OWNR - StarCraft Player Types.

Required for all versions and all game types. Validation: Must be size of 12 bytes.

u8[12]: One byte per player slot (0-11) designating the controller type.

0x00 - Inactive
0x01 - Computer (game) [invalid]
0x02 - Occupied by Human Player [invalid]
0x03 - Rescue Passive
0x04 - Unused
0x05 - Computer
0x06 - Human (Open Slot)
0x07 - Neutral
0x08 - Closed slot [invalid]
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..decoded_chk_section import DecodedChkSection

_NUM_PLAYERS = 12


@dataclasses.dataclass(frozen=True)
class DecodedOwnrSection(DecodedChkSection):
    """Represent OWNR - StarCraft Player Types.

    :param _player_controllers: u8[12] one byte per player slot indicating controller type
    """

    _player_controllers: list[int]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.OWNR

    @property
    def player_controllers(self) -> list[int]:
        return self._player_controllers
