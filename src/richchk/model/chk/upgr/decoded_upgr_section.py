"""UPGR - Classic Upgrade Restrictions.

u8[12][46] player_max_upgrade_levels:   max level per player per upgrade u8[12][46]
player_start_upgrade_levels: starting level per player per upgrade u8[46]
global_max_upgrade_levels:   global max levels per upgrade u8[46]
global_start_upgrade_levels: global starting levels per upgrade u8[12][46]
player_uses_defaults:        0=player overrides, 1=uses global default

Total: 12*46 + 12*46 + 46 + 46 + 12*46 = 552 + 552 + 46 + 46 + 552 = 1748 bytes.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..decoded_chk_section import DecodedChkSection

_NUM_PLAYERS = 12
_NUM_UPGRADES = 46


@dataclasses.dataclass(frozen=True)
class DecodedUpgrSection(DecodedChkSection):
    """Represent UPGR - Classic Upgrade Restrictions.

    :param _player_max_levels: flattened u8[12*46]; index p*46+u
    :param _player_start_levels: flattened u8[12*46]; index p*46+u
    :param _global_max_levels: u8[46] global max levels per upgrade
    :param _global_start_levels: u8[46] global start levels per upgrade
    :param _player_uses_defaults: flattened u8[12*46]; index p*46+u
    """

    _player_max_levels: list[int]
    _player_start_levels: list[int]
    _global_max_levels: list[int]
    _global_start_levels: list[int]
    _player_uses_defaults: list[int]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.UPGR

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
