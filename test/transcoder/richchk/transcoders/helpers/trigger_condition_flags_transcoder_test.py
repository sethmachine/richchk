"""Test TriggerConditionFlagsTranscoder.

U8: Flags.

Bit 0 - Unknown/unused

Bit 1 - Enabled flag. If on, the trigger action/condition is disabled/ignored

Bit 2 - Always display flag.

Bit 3 - Unit properties is used. (Note: This is used in *.trg files)

Bit 4 - Unit type is used. Cleared in "Offset + Mask" EUD conditions. May not be
necessary otherwise? B

Bit 5-7 - Unknown/unused
"""

from richchk.model.richchk.trig.conditions.flags.trigger_condition_flags import (
    TriggerConditionFlags,
)
from richchk.transcoder.richchk.transcoders.helpers.trigger_condition_flags_transcoder import (
    TriggerConditionFlagsTranscoder,
)


def test_it_decodes_expected_flags():
    # corresponds to "unit type is used" and all other flags are 0
    flags = 16
    assert TriggerConditionFlagsTranscoder.decode_flags(flags) == TriggerConditionFlags(
        unit_type_is_used=True
    )
    # corresponds to set all flags to True
    flags = 31
    assert TriggerConditionFlagsTranscoder.decode_flags(flags) == TriggerConditionFlags(
        unknown=True,
        disabled=True,
        always_display=True,
        unit_properties_is_used=True,
        unit_type_is_used=True,
    )
    # corresponds to set all flags to False
    flags = 0
    assert (
        TriggerConditionFlagsTranscoder.decode_flags(flags) == TriggerConditionFlags()
    )


def test_it_encodes_flags():
    # corresponds to 10000 or 16 in binary
    assert (
        TriggerConditionFlagsTranscoder.encode_flags(
            TriggerConditionFlags(unit_type_is_used=True)
        )
        == 16
    )

    # corresponds to 11111 or 31 in binary
    assert (
        TriggerConditionFlagsTranscoder.encode_flags(
            TriggerConditionFlags(
                unknown=True,
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
        TriggerConditionFlagsTranscoder.encode_flags(
            TriggerConditionFlags(
                unknown=True,
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
        TriggerConditionFlagsTranscoder.encode_flags(
            TriggerConditionFlags(
                unknown=True,
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
        TriggerConditionFlagsTranscoder.encode_flags(
            TriggerConditionFlags(
                unknown=False,
                disabled=False,
                always_display=True,
                unit_properties_is_used=False,
                unit_type_is_used=False,
            )
        )
        == 4
    )
    # all flags disabled, 00000
    assert TriggerConditionFlagsTranscoder.encode_flags(TriggerConditionFlags()) == 0
