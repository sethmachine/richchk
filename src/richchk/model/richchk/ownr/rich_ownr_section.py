"""OWNR - StarCraft Player Types.

Required for all versions and all game types. Validation: Must be size of 12 bytes.

u8[12]: One byte per player slot (0-11) designating the controller type.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection
from .player_type import PlayerType


@dataclasses.dataclass(frozen=True)
class RichOwnrSection(RichChkSection):
    """Represent OWNR - StarCraft Player Types.

    :param _player_types: list of PlayerType, one per player slot (12 total)
    """

    _player_types: list[PlayerType]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.OWNR

    @property
    def player_types(self) -> list[PlayerType]:
        return self._player_types
