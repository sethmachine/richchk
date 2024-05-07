"""TRIG - Triggers.  Data structure for a single condition.

16 Conditions (20 byte struct) Every trigger has 16 of the following format, even if
only one condition is used. See the appendix for information on which items are used for
what conditions.

u32: Location number for the condition (1 based -- 0 refers to No Location), EUD Bitmask
for a Death condition if the MaskFlag is set to "SC"

u32: Group that the condition applies to

u32: Qualified number (how many/resource amount)

u16: Unit ID condition applies to

u8: Numeric comparison, switch state

u8: Condition byte

u8: Resource type, score type, Switch number (0-based)

u8: Flags

Bit 0 - Unknown/unused

Bit 1 - Enabled flag. If on, the trigger action/condition is disabled/ignored

Bit 2 - Always display flag.

Bit 3 - Unit properties is used. (Note: This is used in *.trg files)

 Bit 4 - Unit type is used. Cleared in "Offset + Mask" EUD conditions. May not be
necessary otherwise?

Bit 5-7 - Unknown/unused

u16: MaskFlag: set to "SC" (0x53, 0x43) when using the bitmask for EUDs, 0 otherwise
"""

import dataclasses


@dataclasses.dataclass(frozen=True)
class DecodedTriggerCondition:
    """Represent a single decoded condition from TRIG section.

    :param _location_id: u32 - Location number for the condition (1 based -- 0 refers to
        No Location), EUD Bitmask for a Death condition if the MaskFlag is set to "SC"
    :param _group: u32 - Group that the condition applies to
    :param _quantity: u32 - Qualified number (how many/resource amount)
    :param _unit_id: u16 - Unit ID condition applies to
    :param _numeric_comparison_operation: u8 - Numeric comparison, switch state
    :param _condition_id: u8 - Condition byte
    :param _numeric_comparand_type: u8 - Resource type, score type, Switch number
    :param _flags: u8 - Flags - Bit 0 - Unknown/unused - Bit 1 - Enabled flag. If on,
        the trigger action/condition is disabled/ignored - Bit 2 - Always display flag.
        - Bit 3 - Unit properties are used. (Note: This is used in *.trg files) - Bit 4
        - Unit type is used. Cleared in "Offset + Mask" EUD conditions. May not be
        necessary otherwise? - Bit 5-7 - Unknown/unused
    :param _mask_flag: u16 - MaskFlag: set to "SC" (0x53, 0x43) when using the bitmask
        for EUDs, 0 otherwise
    """

    _location_id: int
    _group: int
    _quantity: int
    _unit_id: int
    _numeric_comparison_operation: int
    _condition_id: int
    _numeric_comparand_type: int
    _flags: int
    _mask_flag: int

    @property
    def location_id(self) -> int:
        return self._location_id

    @property
    def group(self) -> int:
        return self._group

    @property
    def quantity(self) -> int:
        return self._quantity

    @property
    def unit_id(self) -> int:
        return self._unit_id

    @property
    def numeric_comparison_operation(self) -> int:
        return self._numeric_comparison_operation

    @property
    def condition_id(self) -> int:
        return self._condition_id

    @property
    def numeric_comparand_type(self) -> int:
        return self._numeric_comparand_type

    @property
    def flags(self) -> int:
        return self._flags

    @property
    def mask_flag(self) -> int:
        return self._mask_flag
