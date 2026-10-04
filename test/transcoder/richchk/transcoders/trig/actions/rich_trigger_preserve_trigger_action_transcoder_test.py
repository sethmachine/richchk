import copy
import pickle

import pytest

from richchk.model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from richchk.model.richchk.mrgn.rich_mrgn_lookup import RichMrgnLookup
from richchk.model.richchk.richchk_decode_context import RichChkDecodeContext
from richchk.model.richchk.richchk_encode_context import RichChkEncodeContext
from richchk.model.richchk.str.rich_str_lookup import RichStrLookup
from richchk.model.richchk.swnm.rich_swnm_lookup import RichSwnmLookup
from richchk.model.richchk.trig.actions.flags.trigger_action_flags import (
    _DEFAULT_TRIGGER_ACTION_FLAGS,
    TriggerActionFlags,
)
from richchk.model.richchk.trig.actions.preserve_trigger_action import PreserveTrigger
from richchk.model.richchk.trig.actions.set_deaths_action import SetDeathsAction
from richchk.model.richchk.trig.conditions.comparators.numeric_comparator import (
    NumericComparator,
)
from richchk.model.richchk.trig.conditions.deaths_condition import DeathsCondition
from richchk.model.richchk.trig.enums.amount_modifier import AmountModifier
from richchk.model.richchk.trig.player_id import PlayerId
from richchk.model.richchk.trig.rich_trig_section import RichTrigSection
from richchk.model.richchk.trig.rich_trigger import RichTrigger
from richchk.model.richchk.unis.unit_id import UnitId
from richchk.model.richchk.uprp.rich_cuwp_lookup import RichCuwpLookup
from richchk.transcoder.chk.transcoders.chk_trig_transcoder import ChkTrigTranscoder
from richchk.transcoder.richchk.transcoders.richchk_trig_transcoder import (
    RichChkTrigTranscoder,
)
from richchk.transcoder.richchk.transcoders.trig.actions.rich_trigger_preserve_trigger_action_transcoder import (  # noqa: E501
    RichTriggerPreserveTriggerActionTranscoder,
)

# bit 2 (always display) + bit 4 (unit type is used), i.e. 0x14, as written by editors
_FLAGS_0X14 = TriggerActionFlags(always_display=True, unit_type_is_used=True)


@pytest.fixture(scope="function")
def decode_context():
    return RichChkDecodeContext(
        _rich_str_lookup=RichStrLookup(_string_by_id_lookup={}, _id_by_string_lookup={})
    )


@pytest.fixture(scope="function")
def encode_context():
    return RichChkEncodeContext(
        _rich_str_lookup=RichStrLookup(
            _string_by_id_lookup={}, _id_by_string_lookup={}
        ),
        _rich_mrgn_lookup=RichMrgnLookup(
            _location_by_id_lookup={}, _id_by_location_lookup={}
        ),
        _rich_swnm_lookup=RichSwnmLookup(
            _switch_by_id_lookup={}, _id_by_switch_lookup={}
        ),
        _rich_cuwp_lookup=RichCuwpLookup(_cuwp_by_id_lookup={}, _id_by_cuwp_lookup={}),
    )


def _decoded_preserve(flags: int) -> DecodedTriggerAction:
    return DecodedTriggerAction(
        _location_id=0,
        _text_string_id=0,
        _wav_string_id=0,
        _time=0,
        _first_group=0,
        _second_group=0,
        _action_argument_type=0,
        _action_id=PreserveTrigger.action_id().id,
        _quantifier_or_switch_or_order=0,
        _flags=flags,
        _padding=0,
        _mask_flag=0,
    )


def test_default_preserve_trigger_is_still_a_singleton():
    assert PreserveTrigger() is PreserveTrigger()
    assert PreserveTrigger().flags is _DEFAULT_TRIGGER_ACTION_FLAGS


def test_preserve_trigger_with_equal_to_default_flags_is_the_singleton():
    assert PreserveTrigger(_flags=TriggerActionFlags()) is PreserveTrigger()


def test_preserve_trigger_accepts_flags():
    action = PreserveTrigger(_flags=_FLAGS_0X14)
    assert action.flags == _FLAGS_0X14
    assert action is not PreserveTrigger()
    assert action != PreserveTrigger()
    assert action == PreserveTrigger(_flags=_FLAGS_0X14)
    assert hash(action) == hash(PreserveTrigger(_flags=_FLAGS_0X14))
    # creating a flagged instance must not corrupt the singleton
    assert PreserveTrigger().flags is _DEFAULT_TRIGGER_ACTION_FLAGS


def test_dataclass_replace_with_flags_works():
    import dataclasses

    replaced = dataclasses.replace(PreserveTrigger(), _flags=_FLAGS_0X14)
    assert replaced == PreserveTrigger(_flags=_FLAGS_0X14)


def test_copy_and_pickle_preserve_default_and_flagged():
    flagged = PreserveTrigger(_flags=_FLAGS_0X14)
    assert copy.copy(PreserveTrigger()) is PreserveTrigger()
    assert copy.deepcopy(PreserveTrigger()) is PreserveTrigger()
    assert copy.deepcopy(flagged) == flagged
    assert pickle.loads(pickle.dumps(PreserveTrigger())) is PreserveTrigger()
    assert pickle.loads(pickle.dumps(flagged)) == flagged


def test_decode_no_flags_returns_singleton(decode_context):
    decoded = RichTriggerPreserveTriggerActionTranscoder().decode(
        _decoded_preserve(0), decode_context
    )
    assert decoded is PreserveTrigger()


@pytest.mark.parametrize("flags_int", [0x02, 0x04, 0x10, 0x12, 0x14, 0x16])
def test_decode_with_flags_does_not_raise_and_round_trips(
    flags_int, decode_context, encode_context
):
    transcoder = RichTriggerPreserveTriggerActionTranscoder()
    decoded = _decoded_preserve(flags_int)
    rich = transcoder.decode(decoded, decode_context)
    assert isinstance(rich, PreserveTrigger)
    assert rich.flags != _DEFAULT_TRIGGER_ACTION_FLAGS
    assert transcoder.encode(rich, encode_context) == decoded


def test_encode_default_preserve_trigger_has_zero_flags(encode_context):
    encoded = RichTriggerPreserveTriggerActionTranscoder().encode(
        PreserveTrigger(), encode_context
    )
    assert encoded == _decoded_preserve(0)


def _trigger_section(preserve: PreserveTrigger, n: int = 3) -> RichTrigSection:
    return RichTrigSection(
        _triggers=[
            RichTrigger(
                _conditions=[
                    DeathsCondition(
                        _group=PlayerId.PLAYER_8,
                        _unit=UnitId.ZERG_SCOURGE,
                        _comparator=NumericComparator.AT_LEAST,
                        _amount=i,
                    )
                ],
                _actions=[
                    SetDeathsAction(
                        _group=PlayerId.PLAYER_1,
                        _unit=UnitId.ZERG_SCOURGE,
                        _amount=i,
                        _amount_modifier=AmountModifier.SET_TO,
                    ),
                    preserve,
                ],
                _players={PlayerId.PLAYER_1},
            )
            for i in range(1, n + 1)
        ]
    )


def _preserve_action_flag_bytes(section_bytes: bytes) -> list[int]:
    triggers = [section_bytes[i : i + 2400] for i in range(0, len(section_bytes), 2400)]
    # actions start after 16 conditions * 20 bytes, 32 bytes each; flags at byte 28
    return [t[320 + 32 * 1 + 28] for t in triggers]


@pytest.mark.parametrize(
    "preserve, expected_flag_byte",
    [(PreserveTrigger(), 0), (PreserveTrigger(_flags=_FLAGS_0X14), 0x14)],
)
def test_trig_section_round_trip_through_batched_optimizer(
    preserve, expected_flag_byte, decode_context, encode_context
):
    section = _trigger_section(preserve)
    transcoder = RichChkTrigTranscoder()
    encoded = ChkTrigTranscoder().encode(
        transcoder.encode(section, encode_context), include_header=False
    )
    assert _preserve_action_flag_bytes(encoded) == [expected_flag_byte] * 3
    decoded_again = transcoder.decode(
        ChkTrigTranscoder().decode(encoded), decode_context
    )
    assert decoded_again == section
