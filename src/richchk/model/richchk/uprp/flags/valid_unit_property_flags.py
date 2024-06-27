"""Valid unit properties flags.

u16: Which elements of the unit data are valid, which properties can be changed by the
map maker.

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
class ValidUnitPropertyFlags(CuwpFlagsBase):
    _owner_play_valid: bool = True
    _hp_valid: bool = True
    _shields_valid: bool = True
    _energy_valid: bool = True
    _resource_amount_valid: bool = True
    _hanger_amount_valid: bool = True
    _unknown_flag: bool = False

    @classmethod
    def flags_bit_size(cls) -> int:
        return 16

    @property
    def owner_play_valid(self) -> bool:
        return self._owner_play_valid

    @property
    def hp_valid(self) -> bool:
        return self._hp_valid

    @property
    def shields_valid(self) -> bool:
        return self._shields_valid

    @property
    def energy_valid(self) -> bool:
        return self._energy_valid

    @property
    def resource_amount_valid(self) -> bool:
        return self._resource_amount_valid

    @property
    def hanger_amount_valid(self) -> bool:
        return self._hanger_amount_valid

    @property
    def unknown_flag(self) -> bool:
        return self._unknown_flag
