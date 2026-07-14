"""PTEC - Classic Tech Restrictions.

u8[12][24] player_tech_availability: 0=unavailable, 1=available per player per tech
u8[12][24] player_tech_researched:   0=not researched, 1=already researched per player
u8[24]     global_tech_availability: global defaults per tech u8[24]
global_tech_researched:   global researched defaults per tech u8[12][24]
player_uses_defaults:     0=player overrides, 1=uses global default

Total: 12*24 + 12*24 + 24 + 24 + 12*24 = 288 + 288 + 24 + 24 + 288 = 912 bytes.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..decoded_chk_section import DecodedChkSection

_NUM_PLAYERS = 12
_NUM_TECHS = 24


@dataclasses.dataclass(frozen=True)
class DecodedPtecSection(DecodedChkSection):
    """Represent PTEC - Classic Tech Restrictions.

    :param _player_tech_availability: flattened u8[12*24]; index p*24+t
    :param _player_tech_researched: flattened u8[12*24]; index p*24+t
    :param _global_tech_availability: u8[24] global defaults per tech
    :param _global_tech_researched: u8[24] global researched defaults per tech
    :param _player_uses_defaults: flattened u8[12*24]; index p*24+t
    """

    _player_tech_availability: list[int]
    _player_tech_researched: list[int]
    _global_tech_availability: list[int]
    _global_tech_researched: list[int]
    _player_uses_defaults: list[int]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.PTEC

    @property
    def player_tech_availability(self) -> list[int]:
        return self._player_tech_availability

    @property
    def player_tech_researched(self) -> list[int]:
        return self._player_tech_researched

    @property
    def global_tech_availability(self) -> list[int]:
        return self._global_tech_availability

    @property
    def global_tech_researched(self) -> list[int]:
        return self._global_tech_researched

    @property
    def player_uses_defaults(self) -> list[int]:
        return self._player_uses_defaults
