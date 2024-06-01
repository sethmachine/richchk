"""UPRP - CUWP - create unit with properties.

Required for all versions. Not required for Melee. Validation: Must be size of 1280
bytes.

This section is used whenever the "create units with properties trigger" is used. Since
a slot has to be assigned to the action, this is where each slot is designated.

There are 64 of the following structures regardless of how many are used, and it cannot
exceed 64.

u16: Flag of which special properties can be applied to unit, and are valid.

Bit 0 - Cloak bit is valid

Bit 1 - Burrowed bit is valid

Bit 2 - In transit bit is valid

Bit 3 - Hallucinated bit is valid

Bit 4 - Invincible bit is valid

Bit 5-15 - Unknown/unused

u16: Which elements of the unit data are valid, which properties can be changed by the
map maker. Bit 0 - Owner player is valid (unit is not neutral)

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

u16: Flags Bit 0 - Unit is cloaked

Bit 1 - Unit is burrowed

Bit 2 - Building is in transit

Bit 3 - Unit is hallucinated

Bit 4 - Unit is invincible

Bit 5-15 - Unknown/unused

u32: Unknown/unused. Padding?
"""

import dataclasses


@dataclasses.dataclass(frozen=True)
class DecodedCuwpSlot:
    """Represent a single decoded create unit with properties slot.

    :param _valid_special_properties_flags: u16 - Flag of which special properties can
        be applied to unit, and are valid. Bit 0 - Cloak bit is valid Bit 1 - Burrowed
        bit is valid Bit 2 - In transit bit is valid Bit 3 - Hallucinated bit is valid
        Bit 4 - Invincible bit is valid Bit 5-15 - Unknown/unused
    :param _valid_unit_properties_flags: u16 - Which elements of the unit data are
        valid, which properties can be changed by the map maker. Bit 0 - Owner player is
        valid (unit is not neutral) Bit 1 - HP is valid Bit 2 - Shields is valid Bit 3 -
        Energy is valid Bit 4 - Resource amount is valid (unit is a resource) Bit 5 -
        Amount in hanger is valid Bit 6 - Unknown/unused
    :param _owner_player: u8 - Player number that owns unit. Will always be NULL in this
        section (0)
    :param _hitpoints_percentage: u8 - Hit point % (1-100)
    :param _shieldpoints_percentage: u8 - Shield point % (1-100)
    :param _energypoints_percentage: u8 - Energy point % (1-100)
    :param _resource_amount: u32 - Resource amount (for resources only)
    :param _units_in_hangar: u16 - # of units in hangar
    :param _flags: u16 - Flags Bit 0 - Unit is cloaked Bit 1 - Unit is burrowed Bit 2 -
        Building is in transit Bit 3 - Unit is hallucinated Bit 4 - Unit is invincible
        Bit 5-15 - Unknown/unused
    :param _padding: u32 - Unknown/unused. Padding?
    """

    _valid_special_properties_flags: int
    _valid_unit_properties_flags: int
    _owner_player: int
    _hitpoints_percentage: int
    _shieldpoints_percentage: int
    _energypoints_percentage: int
    _resource_amount: int
    _units_in_hangar: int
    _flags: int
    _padding: int

    @property
    def valid_special_properties_flags(self) -> int:
        """Flag of which special properties can be applied to unit, and are valid."""
        return self._valid_special_properties_flags

    @property
    def valid_unit_properties_flags(self) -> int:
        """Which elements of the unit data are valid, which properties can be changed by
        the map maker."""
        return self._valid_unit_properties_flags

    @property
    def owner_player(self) -> int:
        """Player number that owns unit.

        Will always be NULL in this section (0).
        """
        return self._owner_player

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
        """# of units in hangar."""
        return self._units_in_hangar

    @property
    def flags(self) -> int:
        """Flags Bit 0 - Unit is cloaked Bit 1 - Unit is burrowed Bit 2 - Building is in
        transit Bit 3 - Unit is hallucinated Bit 4 - Unit is invincible Bit 5-15 -
        Unknown/unused."""
        return self._flags

    @property
    def padding(self) -> int:
        """Unknown/unused.

        Padding?
        """
        return self._padding
