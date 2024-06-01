"""Test TriggerActionFlagsTranscoder.

u8: Flags

Bit 0 - Ignore a wait/transmission once.

Bit 1 - Enabled flag. If on, the trigger action/condition is disabled.

Bit 2 - Always display flag - when not set: if the user has turned off subtitles (see
sound options) the text will not display, when set: text will always display

Bit 3 - Unit properties is used. Staredit uses this for *.trg files.

Bit 4 - Unit type is used. Cleared in "Offset + Mask" EUD actions.

Bit 5-7 - Unknown/unused
"""
from richchk.model.richchk.trig.actions.flags.trigger_action_flags import (
    TriggerActionFlags,
)
from richchk.transcoder.richchk.transcoders.helpers.trigger_action_flags_transcoder import (
    TriggerActionFlagsTranscoder,
)


def test_it_decodes_expected_flags():
    # corresponds to "unit type is used" and all other flags are 0
    flags = 16
    assert TriggerActionFlagsTranscoder.decode_flags(flags) == TriggerActionFlags(
        unit_type_is_used=True
    )
    # corresponds to set all flags to True
    flags = 31
    assert TriggerActionFlagsTranscoder.decode_flags(flags) == TriggerActionFlags(
        ignore_wait_or_transmission_once=True,
        disabled=True,
        always_display=True,
        unit_properties_is_used=True,
        unit_type_is_used=True,
    )
    # corresponds to set all flags to False
    flags = 0
    assert TriggerActionFlagsTranscoder.decode_flags(flags) == TriggerActionFlags()


def test_it_encodes_flags():
    # corresponds to 10000 or 16 in binary
    assert (
        TriggerActionFlagsTranscoder.encode_flags(
            TriggerActionFlags(unit_type_is_used=True)
        )
        == 16
    )

    # corresponds to 11111 or 31 in binary
    assert (
        TriggerActionFlagsTranscoder.encode_flags(
            TriggerActionFlags(
                ignore_wait_or_transmission_once=True,
                disabled=True,
                always_display=True,
                unit_properties_is_used=True,
                unit_type_is_used=True,
            )
        )
        == 31
    )
    # corresponds to every other flag turned off, 10101
    assert (
        TriggerActionFlagsTranscoder.encode_flags(
            TriggerActionFlags(
                ignore_wait_or_transmission_once=True,
                disabled=False,
                always_display=True,
                unit_properties_is_used=False,
                unit_type_is_used=True,
            )
        )
        == 21
    )
    # corresponds to the first 2 flags enabled, last 3 disabled, 00011
    assert (
        TriggerActionFlagsTranscoder.encode_flags(
            TriggerActionFlags(
                ignore_wait_or_transmission_once=True,
                disabled=True,
                always_display=False,
                unit_properties_is_used=False,
                unit_type_is_used=False,
            )
        )
        == 3
    )
    # corresponds to the middle flag enabled, all others disabled, 00100
    assert (
        TriggerActionFlagsTranscoder.encode_flags(
            TriggerActionFlags(
                ignore_wait_or_transmission_once=False,
                disabled=False,
                always_display=True,
                unit_properties_is_used=False,
                unit_type_is_used=False,
            )
        )
        == 4
    )
    # all flags disabled, 00000
    assert TriggerActionFlagsTranscoder.encode_flags(TriggerActionFlags()) == 0
