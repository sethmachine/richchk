"""UPGR - Classic Upgrade Restrictions.

Stores per-player upgrade level restrictions and global upgrade level defaults.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection

_NUM_PLAYERS = 12
_NUM_UPGRADES = 46


@dataclasses.dataclass(frozen=True)
class RichUpgrSection(RichChkSection):
    """Represent UPGR - Classic Upgrade Restrictions.

    :param _player_max_levels: list[list[int]] shape [12][46]
    :param _player_start_levels: list[list[int]] shape [12][46]
    :param _global_max_levels: list[int] length 46
    :param _global_start_levels: list[int] length 46
    :param _player_uses_defaults: list[list[bool]] shape [12][46]; True=use global
        default
    """

    _player_max_levels: list[list[int]]
    _player_start_levels: list[list[int]]
    _global_max_levels: list[int]
    _global_start_levels: list[int]
    _player_uses_defaults: list[list[bool]]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.UPGR

    @property
    def player_max_levels(self) -> list[list[int]]:
        return self._player_max_levels

    @property
    def player_start_levels(self) -> list[list[int]]:
        return self._player_start_levels

    @property
    def global_max_levels(self) -> list[int]:
        return self._global_max_levels

    @property
    def global_start_levels(self) -> list[int]:
        return self._global_start_levels

    @property
    def player_uses_defaults(self) -> list[list[bool]]:
        return self._player_uses_defaults
