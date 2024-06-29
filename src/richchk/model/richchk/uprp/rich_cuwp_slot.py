"""UPRP - CUWP - create unit with properties.

Required for all versions. Not required for Melee. Validation: Must be size of 1280
bytes.

This section is used whenever the create units with properties trigger is used. Since a
slot has to be assigned to the action, this is where each slot is designated.

There are 64 of the following structures regardless of how many are used and it cannot
exceed 64.

u16: Flag of which special properties can be applied to unit, and are valid.

Bit 0 - Cloak bit is valid

Bit 1 - Burrowed bit is valid

Bit 2 - In transit bit is valid

Bit 3 - Hallucinated bit is valid

Bit 4 - Invincible bit is valid

Bit 5-15 - Unknown/unused

u16: Which elements of the unit data are valid, which properties can be changed by the
map maker.

Bit 0 - Owner player is valid (unit is not neutral)

Bit 1 - HP is valid

Bit 2 - Shields is valid

Bit 3 - Energy is valid

Bit 4 - Resource amount is valid (unit is a resource)

Bit 5 - Amount in hanger is valid

Bit 6 - Unknown/unused

u8: Player number that owns unit. Will always be NULL in this section (0)

u8: Hit point % (1-100)

u8: Shield point % (1-100)

u8: Energy point % (1-100)

u32: Resource amount (for resources only)

u16: # of units in hangar

u16: Flags

Bit 0 - Unit is cloaked

Bit 1 - Unit is burrowed

Bit 2 - Building is in transit

Bit 3 - Unit is hallucinated

Bit 4 - Unit is invincible

Bit 5-15 - Unknown/unused

u32: Unknown/unused. Padding?
"""

import dataclasses
from typing import Any, Optional

from .flags.valid_special_property_flags import ValidSpecialPropertyFlags
from .flags.valid_unit_property_flags import ValidUnitPropertyFlags


@dataclasses.dataclass(frozen=True)
class _RichCuwpSlotFlagsData:
    _valid_special_property_flags: ValidSpecialPropertyFlags = (
        ValidSpecialPropertyFlags()
    )
    _valid_unit_property_flags: ValidUnitPropertyFlags = ValidUnitPropertyFlags()
    _unknown_flag: bool = False
    _padding: int = 0

    @property
    def valid_special_property_flags(self) -> ValidSpecialPropertyFlags:
        return self._valid_special_property_flags

    @property
    def valid_unit_property_flags(self) -> ValidUnitPropertyFlags:
        return self._valid_unit_property_flags

    @property
    def unknown_flag(self) -> bool:
        return self._unknown_flag

    @property
    def padding(self) -> int:
        return self._padding


@dataclasses.dataclass(frozen=True)
class RichCuwpSlot:
    _hitpoints_percentage: int
    _shieldpoints_percentage: int
    _energypoints_percentage: int
    _resource_amount: int = 0
    _units_in_hangar: int = 0
    _cloaked: bool = False
    _burrowed: bool = False
    _building_in_transit: bool = False
    _hallucinated: bool = False
    _invincible: bool = False
    _flags_data: _RichCuwpSlotFlagsData = _RichCuwpSlotFlagsData()
    _index: Optional[int] = None

    def __eq__(self, other: object) -> bool:
        # 2 CUWPs are equal if all the fields are the same excluding the index
        # there's never a reason to duplicate a CUWP, so don't allow this
        if isinstance(other, RichCuwpSlot):
            return self._get_fields_for_equality() == other._get_fields_for_equality()
        return False

    def __hash__(self) -> int:
        # CUWP hashes ignores the index
        return hash(self._get_fields_for_equality())

    def _get_fields_for_equality(self) -> tuple[Any]:
        return tuple(
            (
                getattr(self, field.name)
                for field in dataclasses.fields(self)
                if field.name != "_index"
            )
        )

    @property
    def hitpoints_percentage(self) -> int:
        """Hit point % (1-100)."""
        return self._hitpoints_percentage

    @property
    def shieldpoints_percentage(self) -> int:
        """Shield point % (1-100)."""
        return self._shieldpoints_percentage

    @property
    def energypoints_percentage(self) -> int:
        """Energy point % (1-100)."""
        return self._energypoints_percentage

    @property
    def resource_amount(self) -> int:
        """Resource amount (for resources only)."""
        return self._resource_amount

    @property
    def units_in_hangar(self) -> int:
        """Number of units in hangar."""
        return self._units_in_hangar

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
    def flags_data(self) -> _RichCuwpSlotFlagsData:
        """Flags data."""
        return self._flags_data

    @property
    def index(self) -> Optional[int]:
        """Slot used in CUWP."""
        return self._index
