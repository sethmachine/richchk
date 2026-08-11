"""Transcode flags data found on each mission briefing action."""
from .....model.richchk.mbrf.actions.flags.briefing_action_flags import (
    BriefingActionFlags,
)
from .....util import logger


class BriefingActionFlagsTranscoder:
    _LOG = logger.get_logger("BriefingActionFlagsTranscoder")
    _HIGHEST_EXPECTED_FLAGS_VALUE = 31

    @classmethod
    def decode_flags(cls, action_flags: int) -> BriefingActionFlags:
        bit_string = "{:08b}".format(action_flags)
        if action_flags > cls._HIGHEST_EXPECTED_FLAGS_VALUE:
            cls._LOG.warning(
                f"A briefing action has flags with a value greater than expected: "
                f"{action_flags} is greater than {cls._HIGHEST_EXPECTED_FLAGS_VALUE}"
            )
        return BriefingActionFlags(
            ignore_wait_or_transmission_once=bool(int(bit_string[-1])),
            disabled=bool(int(bit_string[-2])),
            always_display=bool(int(bit_string[-3])),
            unit_properties_is_used=bool(int(bit_string[-4])),
            unit_type_is_used=bool(int(bit_string[-5])),
        )

    @classmethod
    def encode_flags(cls, encoded_flags: BriefingActionFlags) -> int:
        return (
            int(encoded_flags.ignore_wait_or_transmission_once)
            | (int(encoded_flags.disabled) << 1)
            | (int(encoded_flags.always_display) << 2)
            | (int(encoded_flags.unit_properties_is_used) << 3)
            | (int(encoded_flags.unit_type_is_used) << 4)
        )
