"""PUNI - Player Unit Restrictions.

Stores per-player unit availability overrides and global unit availability defaults.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection

_NUM_PLAYERS = 12
_NUM_UNITS = 228


@dataclasses.dataclass(frozen=True)
class RichPuniSection(RichChkSection):
    """Represent PUNI - Player Unit Restrictions.

    :param _player_unit_availability: list[list[bool]] shape [12][228]; True=available
    :param _global_unit_availability: list[bool] length 228; global defaults
    :param _player_uses_defaults: list[list[bool]] shape [12][228]; True=use global
        default
    """

    _player_unit_availability: list[list[bool]]
    _global_unit_availability: list[bool]
    _player_uses_defaults: list[list[bool]]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.PUNI

    @property
    def player_unit_availability(self) -> list[list[bool]]:
        return self._player_unit_availability

    @property
    def global_unit_availability(self) -> list[bool]:
        return self._global_unit_availability

    @property
    def player_uses_defaults(self) -> list[list[bool]]:
        return self._player_uses_defaults
