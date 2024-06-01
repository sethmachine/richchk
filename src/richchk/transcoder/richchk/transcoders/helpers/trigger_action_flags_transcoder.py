"""Transcode flags data found on each trigger action.

u8: Flags

Bit 0 - Ignore a wait/transmission once.

Bit 1 - Enabled flag. If on, the trigger action/condition is disabled.

Bit 2 - Always display flag - when not set: if the user has turned off subtitles (see
sound options) the text will not display, when set: text will always display

Bit 3 - Unit properties is used. Staredit uses this for *.trg files.

Bit 4 - Unit type is used. Cleared in "Offset + Mask" EUD actions.

Bit 5-7 - Unknown/unused
"""
from .....model.richchk.trig.actions.flags.trigger_action_flags import (
    TriggerActionFlags,
)
from .....util import logger


class TriggerActionFlagsTranscoder:
    _LOG = logger.get_logger("TriggerActionFlagsTranscoder")
    # corresponds to 11111.  Bits in higher positions are unused
    _HIGHEST_EXPECTED_FLAGS_VALUE = 31
    _HIGHEST_BIT = 5

    @classmethod
    def decode_flags(cls, action_flags: int) -> TriggerActionFlags:
        condition_flags_bit_string = "{:08b}".format(action_flags)
        # Starcraft bit string is read right to left, so the first bit
        # is the last position in the bit string, etc.
        # bit of 1 means the elevation is disabled, 0 is enabled
        if action_flags > cls._HIGHEST_EXPECTED_FLAGS_VALUE:
            cls._LOG.warning(
                f"An action has flags with a value greater than expected: "
                f"{action_flags} is greater than {cls._HIGHEST_EXPECTED_FLAGS_VALUE}"
            )
        return TriggerActionFlags(
            ignore_wait_or_transmission_once=bool(int(condition_flags_bit_string[-1])),
            disabled=bool(int(condition_flags_bit_string[-2])),
            always_display=bool(int(condition_flags_bit_string[-3])),
            unit_properties_is_used=bool(int(condition_flags_bit_string[-4])),
            unit_type_is_used=bool(int(condition_flags_bit_string[-5])),
        )

    @classmethod
    def encode_flags(cls, encoded_flags: TriggerActionFlags) -> int:
        return int(
            f"{int(encoded_flags.unit_type_is_used)}"
            f"{int(encoded_flags.unit_properties_is_used)}"
            f"{int(encoded_flags.always_display)}"
            f"{int(encoded_flags.disabled)}"
            f"{int(encoded_flags.ignore_wait_or_transmission_once)}",
            base=2,
        )
