"""FORC - Force Settings.

Not required. Total size: 20 bytes (or less; missing bytes default to 0).

u8[8]:  Force assignment per player slot (0-7); values 0-3 indicate which force.
u16[4]: String index of each force's name (4 forces); 0 means default name.
u8[4]:  Property flags per force.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection
from .force_id import ForceId
from .rich_force import RichForce


@dataclasses.dataclass(frozen=True)
class RichForcSection(RichChkSection):
    """Represent FORC - Force Settings.

    :param _player_force_assignments: list of ForceId, one per player slot (8 total);
        indicates which force each player belongs to
    :param _forces: list of 4 RichForce objects, one per force slot
    """

    _player_force_assignments: list[ForceId]
    _forces: list[RichForce]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.FORC

    @property
    def player_force_assignments(self) -> list[ForceId]:
        return self._player_force_assignments

    @property
    def forces(self) -> list[RichForce]:
        return self._forces
