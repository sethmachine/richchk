"""Transcode flags data found on each trigger condition.

u8: Flags

Bit 0 - Unknown/unused

Bit 1 - Enabled flag. If on, the trigger action/condition is disabled/ignored

Bit 2 - Always display flag.

Bit 3 - Unit properties is used. (Note: This is used in *.trg files)

Bit 4 - Unit type is used. Cleared in "Offset + Mask" EUD conditions. May not be
necessary otherwise? B

Bit 5-7 - Unknown/unused
"""

from .....model.richchk.trig.conditions.flags.trigger_condition_flags import (
    TriggerConditionFlags,
)
from .....util import logger


class TriggerConditionFlagsTranscoder:
    _LOG = logger.get_logger("TriggerConditionFlagsTranscoder")
    # corresponds to 11111.  Bits in higher positions are unused
    _HIGHEST_EXPECTED_FLAGS_VALUE = 31
    _HIGHEST_BIT = 5

    @classmethod
    def decode_flags(cls, condition_flags: int) -> TriggerConditionFlags:
        condition_flags_bit_string = "{:08b}".format(condition_flags)
        # Starcraft bit string is read right to left, so the first bit
        # is the last position in the bit string, etc.
        # bit of 1 means the elevation is disabled, 0 is enabled
        if condition_flags > cls._HIGHEST_EXPECTED_FLAGS_VALUE:
            cls._LOG.warning(
                f"A condition has flags with a value greater than expected: "
                f"{condition_flags} is greater than {cls._HIGHEST_EXPECTED_FLAGS_VALUE}"
            )
        unused_flag = bool(int(condition_flags_bit_string[-1]))
        if unused_flag:
            cls._LOG.warning(
                "The unused/unknown flag is set for this condition's flags.  It is expected to never be set!"
            )
        return TriggerConditionFlags(
            unknown=unused_flag,
            disabled=bool(int(condition_flags_bit_string[-2])),
            always_display=bool(int(condition_flags_bit_string[-3])),
            unit_properties_is_used=bool(int(condition_flags_bit_string[-4])),
            unit_type_is_used=bool(int(condition_flags_bit_string[-5])),
        )

    @classmethod
    def encode_flags(cls, encoded_flags: TriggerConditionFlags) -> int:
        return int(
            f"{int(encoded_flags.unit_type_is_used)}"
            f"{int(encoded_flags.unit_properties_is_used)}"
            f"{int(encoded_flags.always_display)}"
            f"{int(encoded_flags.disabled)}"
            f"{int(encoded_flags.unknown)}",
            base=2,
        )
