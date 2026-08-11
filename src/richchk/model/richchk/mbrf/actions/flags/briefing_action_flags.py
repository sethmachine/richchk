"""Represent flags data found on each mission briefing action.

u8: Flags

Bit 0 - Ignore a wait/transmission once.

Bit 1 - Enabled flag. If on, the action is disabled.

Bit 2 - Always display flag - when not set: if the user has turned off subtitles the
text will not display, when set: text will always display

Bit 3 - Unit properties is used.

Bit 4 - Unit type is used.

Bit 5-7 - Unknown/unused
"""
import dataclasses


@dataclasses.dataclass(frozen=True)
class BriefingActionFlags:
    ignore_wait_or_transmission_once: bool = False
    disabled: bool = False
    always_display: bool = False
    unit_properties_is_used: bool = False
    unit_type_is_used: bool = False


_DEFAULT_BRIEFING_ACTION_FLAGS = BriefingActionFlags()
