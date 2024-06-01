"""Represent flags data found on each trigger condition.

u8: Flags Bit 0 - Unknown/unused

Bit 1 - Enabled flag. If on, the trigger action/condition is disabled/ignored

Bit 2 - Always display flag.

Bit 3 - Unit properties is used. (Note: This is used in *.trg files)

Bit 4 - Unit type is used. Cleared in "Offset + Mask" EUD conditions. May not be
necessary otherwise? B

Bit 5-7 - Unknown/unused
"""
import dataclasses


@dataclasses.dataclass(frozen=True)
class TriggerConditionFlags:
    unknown: bool = False
    disabled: bool = False
    always_display: bool = False
    unit_properties_is_used: bool = False
    unit_type_is_used: bool = False
