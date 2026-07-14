"""PTEC - Classic Tech Restrictions.

Stores per-player tech availability and researched state, plus global defaults.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection
from ..techs.tech_id import TechId
from ..trig.player_id import PlayerId


@dataclasses.dataclass(frozen=True)
class RichPtecSection(RichChkSection):
    """Represent PTEC - Classic Tech Restrictions.

    :param _player_tech_availability: dict[PlayerId, dict[TechId, bool]]
    :param _player_tech_researched: dict[PlayerId, dict[TechId, bool]]
    :param _global_tech_availability: dict[TechId, bool]
    :param _global_tech_researched: dict[TechId, bool]
    :param _player_uses_defaults: dict[PlayerId, dict[TechId, bool]]; True=use global
        default
    """

    _player_tech_availability: dict[PlayerId, dict[TechId, bool]]
    _player_tech_researched: dict[PlayerId, dict[TechId, bool]]
    _global_tech_availability: dict[TechId, bool]
    _global_tech_researched: dict[TechId, bool]
    _player_uses_defaults: dict[PlayerId, dict[TechId, bool]]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.PTEC

    @property
    def player_tech_availability(self) -> dict[PlayerId, dict[TechId, bool]]:
        return self._player_tech_availability

    @property
    def player_tech_researched(self) -> dict[PlayerId, dict[TechId, bool]]:
        return self._player_tech_researched

    @property
    def global_tech_availability(self) -> dict[TechId, bool]:
        return self._global_tech_availability

    @property
    def global_tech_researched(self) -> dict[TechId, bool]:
        return self._global_tech_researched

    @property
    def player_uses_defaults(self) -> dict[PlayerId, dict[TechId, bool]]:
        return self._player_uses_defaults
