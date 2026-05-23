"""FORC - Force Settings.

Not required. Total size: 20 bytes (or less; missing bytes default to 0).

u8[8]:  Force assignment per player slot (0-7); values 0-3 indicate which force.
u16[4]: String index of each force's name (4 forces); 0 means default name.
u8[4]:  Property flags per force.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection
from .rich_force import RichForce


@dataclasses.dataclass(frozen=True)
class RichForcSection(RichChkSection):
    """Represent FORC - Force Settings.

    :param _player_force_assignments: list of force indices (0-3) for each of the 8
        player slots; index indicates which force that player belongs to
    :param _forces: list of 4 RichForce objects, one per force slot
    """

    _player_force_assignments: list[int]
    _forces: list[RichForce]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.FORC

    @property
    def player_force_assignments(self) -> list[int]:
        return self._player_force_assignments

    @property
    def forces(self) -> list[RichForce]:
        return self._forces
