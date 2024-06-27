"""Unit property flags.

u16: Flags

Bit 0 - Unit is cloaked

Bit 1 - Unit is burrowed

Bit 2 - Building is in transit

Bit 3 - Unit is hallucinated

Bit 4 - Unit is invincible

Bit 5-15 - Unknown/unused
"""

import dataclasses

from .cuwp_flags_base import CuwpFlagsBase


@dataclasses.dataclass(frozen=True)
class UnitPropertyFlags(CuwpFlagsBase):
    _cloaked: bool = False
    _burrowed: bool = False
    _building_in_transit: bool = False
    _hallucinated: bool = False
    _invincible: bool = False
    _unknown_flag: bool = False

    @classmethod
    def flags_bit_size(cls) -> int:
        return 16

    @property
    def cloaked(self) -> bool:
        """Unit is cloaked."""
        return self._cloaked

    @property
    def burrowed(self) -> bool:
        """Unit is burrowed."""
        return self._burrowed

    @property
    def building_in_transit(self) -> bool:
        """Building is in transit."""
        return self._building_in_transit

    @property
    def hallucinated(self) -> bool:
        """Unit is hallucinated."""
        return self._hallucinated

    @property
    def invincible(self) -> bool:
        """Unit is invincible."""
        return self._invincible

    @property
    def unknown_flag(self) -> bool:
        return self._unknown_flag
