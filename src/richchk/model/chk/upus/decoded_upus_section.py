"""UPUS - CUWP Slots Used.

Not Required.

This section goes along with the "UPRP" section. This section just indicates which of
the 64 unit properties slot are used.

u8[64]: 1 byte for each trigger unit properties slot

00 - Properties slot is unused

01 - Properties slot is used
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..decoded_chk_section import DecodedChkSection


@dataclasses.dataclass(frozen=True)
class DecodedUpusSection(DecodedChkSection):
    """Represent UPUS - CUWP Slots Used.

    :param _cuwp_slots_used: u8[64] 1 byte for each trigger unit properties slot. 00 -
        Properties slot is unused 01 - Properties slot is used
    """

    _cuwp_slots_used: list[int]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.UPUS

    @property
    def cuwp_slots_used(self) -> list[int]:
        return self._cuwp_slots_used.copy()
