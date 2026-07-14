"""UPGR - Classic Upgrade Restrictions.

Stores per-player upgrade level restrictions and global upgrade level defaults.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection
from ..trig.player_id import PlayerId
from ..upgrades.upgrade_id import UpgradeId


@dataclasses.dataclass(frozen=True)
class RichUpgrSection(RichChkSection):
    """Represent UPGR - Classic Upgrade Restrictions.

    :param _player_max_levels: dict[PlayerId, dict[UpgradeId, int]]
    :param _player_start_levels: dict[PlayerId, dict[UpgradeId, int]]
    :param _global_max_levels: dict[UpgradeId, int]
    :param _global_start_levels: dict[UpgradeId, int]
    :param _player_uses_defaults: dict[PlayerId, dict[UpgradeId, bool]]; True=use global
        default
    """

    _player_max_levels: dict[PlayerId, dict[UpgradeId, int]]
    _player_start_levels: dict[PlayerId, dict[UpgradeId, int]]
    _global_max_levels: dict[UpgradeId, int]
    _global_start_levels: dict[UpgradeId, int]
    _player_uses_defaults: dict[PlayerId, dict[UpgradeId, bool]]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.UPGR

    @property
    def player_max_levels(self) -> dict[PlayerId, dict[UpgradeId, int]]:
        return self._player_max_levels

    @property
    def player_start_levels(self) -> dict[PlayerId, dict[UpgradeId, int]]:
        return self._player_start_levels

    @property
    def global_max_levels(self) -> dict[UpgradeId, int]:
        return self._global_max_levels

    @property
    def global_start_levels(self) -> dict[UpgradeId, int]:
        return self._global_start_levels

    @property
    def player_uses_defaults(self) -> dict[PlayerId, dict[UpgradeId, bool]]:
        return self._player_uses_defaults
