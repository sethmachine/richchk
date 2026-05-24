"""FORC - Force Settings.

Not required. Total size: 20 bytes (or less; missing bytes default to 0).

u8[8]:  Force assignment per player slot (0-7); values 0-3 indicate which force. u16[4]:
String index of each force's name (4 forces); 0 means default name. u8[4]:  Property
flags per force.

Force property flags (per u8):   Bit 0 - Random start location   Bit 1 - Allies   Bit 2
- Allied victory   Bit 3 - Shared vision   Bits 4-7 - Unused
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..decoded_chk_section import DecodedChkSection

_NUM_PLAYERS = 8
_NUM_FORCES = 4


@dataclasses.dataclass(frozen=True)
class DecodedForcSection(DecodedChkSection):
    """Represent FORC - Force Settings.

    :param _player_force_assignments: u8[8] force index (0-3) for each player slot
    :param _force_name_string_ids: u16[4] string index for each force's name
    :param _force_flags: u8[4] property flags for each force
    """

    _player_force_assignments: list[int]
    _force_name_string_ids: list[int]
    _force_flags: list[int]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.FORC

    @property
    def player_force_assignments(self) -> list[int]:
        return self._player_force_assignments

    @property
    def force_name_string_ids(self) -> list[int]:
        return self._force_name_string_ids

    @property
    def force_flags(self) -> list[int]:
        return self._force_flags
