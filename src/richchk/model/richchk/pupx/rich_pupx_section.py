"""PUPx - Brood War Upgrade Restrictions.

Same structure as UPGR but for all 61 upgrades (0-60).
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection

_NUM_PLAYERS = 12
_NUM_UPGRADES = 61


@dataclasses.dataclass(frozen=True)
class RichPupxSection(RichChkSection):
    """Represent PUPx - Brood War Upgrade Restrictions.

    :param _player_max_levels: list[list[int]] shape [12][61]
    :param _player_start_levels: list[list[int]] shape [12][61]
    :param _global_max_levels: list[int] length 61
    :param _global_start_levels: list[int] length 61
    :param _player_uses_defaults: list[list[bool]] shape [12][61]; True=use global
        default
    """

    _player_max_levels: list[list[int]]
    _player_start_levels: list[list[int]]
    _global_max_levels: list[int]
    _global_start_levels: list[int]
    _player_uses_defaults: list[list[bool]]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.PUPX

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
