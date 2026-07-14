"""PUNI - Player Unit Restrictions.

Stores per-player unit availability overrides and global unit availability defaults.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection
from ..trig.player_id import PlayerId
from ..unis.unit_id import UnitId


@dataclasses.dataclass(frozen=True)
class RichPuniSection(RichChkSection):
    """Represent PUNI - Player Unit Restrictions.

    :param _player_unit_availability: dict[PlayerId, dict[UnitId, bool]]; True=available
    :param _global_unit_availability: dict[UnitId, bool]; global defaults
    :param _player_uses_defaults: dict[PlayerId, dict[UnitId, bool]]; True=use global
        default
    """

    _player_unit_availability: dict[PlayerId, dict[UnitId, bool]]
    _global_unit_availability: dict[UnitId, bool]
    _player_uses_defaults: dict[PlayerId, dict[UnitId, bool]]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.PUNI

    @property
    def player_unit_availability(self) -> dict[PlayerId, dict[UnitId, bool]]:
        return self._player_unit_availability

    @property
    def global_unit_availability(self) -> dict[UnitId, bool]:
        return self._global_unit_availability

    @property
    def player_uses_defaults(self) -> dict[PlayerId, dict[UnitId, bool]]:
        return self._player_uses_defaults
