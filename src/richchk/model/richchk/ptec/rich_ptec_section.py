"""PTEC - Classic Tech Restrictions.

Stores per-player tech availability and researched state, plus global defaults.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection

_NUM_PLAYERS = 12
_NUM_TECHS = 24


@dataclasses.dataclass(frozen=True)
class RichPtecSection(RichChkSection):
    """Represent PTEC - Classic Tech Restrictions.

    :param _player_tech_availability: list[list[bool]] shape [12][24]
    :param _player_tech_researched: list[list[bool]] shape [12][24]
    :param _global_tech_availability: list[bool] length 24
    :param _global_tech_researched: list[bool] length 24
    :param _player_uses_defaults: list[list[bool]] shape [12][24]; True=use global
        default
    """

    _player_tech_availability: list[list[bool]]
    _player_tech_researched: list[list[bool]]
    _global_tech_availability: list[bool]
    _global_tech_researched: list[bool]
    _player_uses_defaults: list[list[bool]]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.PTEC

    @property
    def player_tech_availability(self) -> list[list[bool]]:
        return self._player_tech_availability

    @property
    def player_tech_researched(self) -> list[list[bool]]:
        return self._player_tech_researched

    @property
    def global_tech_availability(self) -> list[bool]:
        return self._global_tech_availability

    @property
    def global_tech_researched(self) -> list[bool]:
        return self._global_tech_researched

    @property
    def player_uses_defaults(self) -> list[list[bool]]:
        return self._player_uses_defaults
