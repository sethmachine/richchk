"""PUNI - Player Unit Restrictions.

u8[12][228] player_unit_availability: 0=unavailable, 1=available (per-player override)
u8[228]     global_unit_availability:  0=unavailable, 1=available (global defaults)
u8[12][228] player_uses_defaults:      0=player overrides, 1=uses global default

Total: 12*228 + 228 + 12*228 = 2736 + 228 + 2736 = 5700 bytes.

Data is stored row-major: first 228 bytes = player 0 availability for all 228 units,
etc.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..decoded_chk_section import DecodedChkSection

_NUM_PLAYERS = 12
_NUM_UNITS = 228


@dataclasses.dataclass(frozen=True)
class DecodedPuniSection(DecodedChkSection):
    """Represent PUNI - Player Unit Restrictions.

    :param _player_unit_availability: flattened u8[12*228];
        player_unit_availability[p*228+u]
    :param _global_unit_availability: u8[228] global defaults per unit
    :param _player_uses_defaults: flattened u8[12*228]; player_uses_defaults[p*228+u]
    """

    _player_unit_availability: list[int]
    _global_unit_availability: list[int]
    _player_uses_defaults: list[int]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.PUNI

    @property
    def player_unit_availability(self) -> list[int]:
        return self._player_unit_availability

    @property
    def global_unit_availability(self) -> list[int]:
        return self._global_unit_availability

    @property
    def player_uses_defaults(self) -> list[int]:
        return self._player_uses_defaults
