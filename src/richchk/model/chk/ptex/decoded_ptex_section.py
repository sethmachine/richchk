"""PTEx - Brood War Tech Restrictions.

u8[12][44] player_tech_availability: 0=unavailable, 1=available per player per tech
u8[12][44] player_tech_researched:   0=not researched, 1=already researched per player
u8[44]     global_tech_availability: global defaults per tech u8[44]
global_tech_researched:   global researched defaults per tech u8[12][44]
player_uses_defaults:     0=player overrides, 1=uses global default

Total: 12*44 + 12*44 + 44 + 44 + 12*44 = 528 + 528 + 44 + 44 + 528 = 1672 bytes.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..decoded_chk_section import DecodedChkSection

_NUM_PLAYERS = 12
_NUM_TECHS = 44


@dataclasses.dataclass(frozen=True)
class DecodedPtexSection(DecodedChkSection):
    """Represent PTEx - Brood War Tech Restrictions.

    :param _player_tech_availability: flattened u8[12*44]; index p*44+t
    :param _player_tech_researched: flattened u8[12*44]; index p*44+t
    :param _global_tech_availability: u8[44] global defaults per tech
    :param _global_tech_researched: u8[44] global researched defaults per tech
    :param _player_uses_defaults: flattened u8[12*44]; index p*44+t
    """

    _player_tech_availability: list[int]
    _player_tech_researched: list[int]
    _global_tech_availability: list[int]
    _global_tech_researched: list[int]
    _player_uses_defaults: list[int]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.PTEX

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
