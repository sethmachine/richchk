"""PUPx - Brood War Upgrade Restrictions.

Same structure as UPGR but for all 61 upgrades (0-60) instead of 46.

u8[12][61] player_max_upgrade_levels:   max level per player per upgrade u8[12][61]
player_start_upgrade_levels: starting level per player per upgrade u8[61]
global_max_upgrade_levels:   global max levels per upgrade u8[61]
global_start_upgrade_levels: global starting levels per upgrade u8[12][61]
player_uses_defaults:        0=player overrides, 1=uses global default

Total: 12*61 + 12*61 + 61 + 61 + 12*61 = 732 + 732 + 61 + 61 + 732 = 2318 bytes.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..decoded_chk_section import DecodedChkSection

_NUM_PLAYERS = 12
_NUM_UPGRADES = 61


@dataclasses.dataclass(frozen=True)
class DecodedPupxSection(DecodedChkSection):
    """Represent PUPx - Brood War Upgrade Restrictions.

    :param _player_max_levels: flattened u8[12*61]; index p*61+u
    :param _player_start_levels: flattened u8[12*61]; index p*61+u
    :param _global_max_levels: u8[61] global max levels per upgrade
    :param _global_start_levels: u8[61] global start levels per upgrade
    :param _player_uses_defaults: flattened u8[12*61]; index p*61+u
    """

    _player_max_levels: list[int]
    _player_start_levels: list[int]
    _global_max_levels: list[int]
    _global_start_levels: list[int]
    _player_uses_defaults: list[int]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.PUPX

    @property
    def player_max_levels(self) -> list[int]:
        return self._player_max_levels

    @property
    def player_start_levels(self) -> list[int]:
        return self._player_start_levels

    @property
    def global_max_levels(self) -> list[int]:
        return self._global_max_levels

    @property
    def global_start_levels(self) -> list[int]:
        return self._global_start_levels

    @property
    def player_uses_defaults(self) -> list[int]:
        return self._player_uses_defaults
