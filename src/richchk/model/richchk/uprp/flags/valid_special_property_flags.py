"""Valid special properties flags.

u16: Flag of which special properties can be applied to unit, and are valid.

Bit 0 - Owner player is valid (unit is not neutral)

Bit 1 - HP is valid

Bit 2 - Shields is valid

Bit 3 - Energy is valid

Bit 4 - Resource amount is valid (unit is a resource)

Bit 5 - Amount in hanger is valid

Bit 6 - Unknown/unused
"""

import dataclasses

from .cuwp_flags_base import CuwpFlagsBase


@dataclasses.dataclass(frozen=True)
class ValidSpecialPropertyFlags(CuwpFlagsBase):
    _cloak_valid: bool = True
    _burrowed_valid: bool = True
    _in_transit_valid: bool = True
    _hallucinated_valid: bool = True
    _invincible_valid: bool = True
    _unknown_flag: bool = False

    @classmethod
    def flags_bit_size(cls) -> int:
        return 16

    @property
    def cloak_valid(self) -> bool:
        return self._cloak_valid

    @property
    def burrowed_valid(self) -> bool:
        return self._burrowed_valid

    @property
    def in_transit_valid(self) -> bool:
        return self._in_transit_valid

    @property
    def hallucinated_valid(self) -> bool:
        return self._hallucinated_valid

    @property
    def invincible_valid(self) -> bool:
        return self._invincible_valid

    @property
    def unknown_flag(self) -> bool:
        return self._unknown_flag
