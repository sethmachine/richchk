import logging

import pytest

from richchk.model.chk.trig.decoded_player_execution import DecodedPlayerExecution
from richchk.model.chk.trig.decoded_trigger import DecodedTrigger
from richchk.model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from richchk.model.chk.trig.decoded_trigger_condition import DecodedTriggerCondition
from richchk.model.richchk.mrgn.rich_mrgn_lookup import RichMrgnLookup
from richchk.model.richchk.richchk_decode_context import RichChkDecodeContext
from richchk.model.richchk.richchk_encode_context import RichChkEncodeContext
from richchk.model.richchk.str.rich_str_lookup import RichStrLookup
from richchk.model.richchk.swnm.rich_swnm_lookup import RichSwnmLookup
from richchk.model.richchk.trig.actions.preserve_trigger_action import PreserveTrigger
from richchk.model.richchk.trig.actions.set_doodad_state_action import (
    SetDoodadStateAction,
)
from richchk.model.richchk.trig.conditions.deaths_condition import DeathsCondition
from richchk.model.richchk.trig.trigger_action_id import TriggerActionId
from richchk.model.richchk.trig.trigger_condition_id import TriggerConditionId
from richchk.model.richchk.uprp.rich_cuwp_lookup import RichCuwpLookup
from richchk.transcoder.richchk.transcoders.richchk_trig_transcoder import (
    RichChkTrigTranscoder,
)


def _action(action_id: TriggerActionId, **fields) -> DecodedTriggerAction:
    values = dict(
        _location_id=0,
        _text_string_id=0,
        _wav_string_id=0,
        _time=0,
        _first_group=0,
        _second_group=0,
        _action_argument_type=0,
        _action_id=action_id.id,
        _quantifier_or_switch_or_order=0,
        _flags=0,
        _padding=0,
        _mask_flag=0,
    )
    values.update(fields)
    return DecodedTriggerAction(**values)


def _condition(condition_id: TriggerConditionId, **fields) -> DecodedTriggerCondition:
    values = dict(
        _location_id=0,
        _group=0,
        _quantity=0,
        _unit_id=0,
        _numeric_comparison_operation=0,
        _condition_id=condition_id.id,
        _numeric_comparand_type=0,
        _flags=0,
        _mask_flag=0,
    )
    values.update(fields)
    return DecodedTriggerCondition(**values)


@pytest.fixture(scope="function")
def junk_doodad_action():
    return _action(
        TriggerActionId.SET_DOODAD_STATE,
        _first_group=255,
        _action_argument_type=255,
        _quantifier_or_switch_or_order=255,
        _text_string_id=7,
    )


@pytest.fixture(scope="function")
def junk_deaths_condition():
    return _condition(TriggerConditionId.DEATHS, _unit_id=65535, _quantity=3)


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


def _trigger(conditions, actions) -> DecodedTrigger:
    return DecodedTrigger(
        _conditions=conditions,
        _actions=actions,
        _player_execution=DecodedPlayerExecution(
            _execution_flags=0,
            _player_flags=[1] + [0] * 26,
            _current_action_index=0,
        ),
    )


def test_it_keeps_the_raw_action_and_logs_an_error_when_a_rich_action_cannot_be_decoded(
    junk_doodad_action, decode_context, caplog
):
    with caplog.at_level(logging.ERROR):
        result = RichChkTrigTranscoder()._decode_single_action(
            junk_doodad_action, decode_context, 7
        )
    assert result is junk_doodad_action
    messages = [
        r.getMessage() for r in caplog.records if "Failed to decode" in r.getMessage()
    ]
    assert len(messages) == 1
    assert "SET_DOODAD_STATE" in messages[0]
    assert "trigger 7" in messages[0]
    assert "written back unchanged" in messages[0]


def test_it_keeps_the_raw_condition_and_logs_an_error_when_a_rich_condition_cannot_be_decoded(
    junk_deaths_condition, decode_context, caplog
):
    with caplog.at_level(logging.ERROR):
        result = RichChkTrigTranscoder()._decode_single_condition(
            junk_deaths_condition, decode_context, 3
        )
    assert result is junk_deaths_condition
    messages = [
        r.getMessage() for r in caplog.records if "Failed to decode" in r.getMessage()
    ]
    assert len(messages) == 1
    assert "DEATHS" in messages[0]
    assert "trigger 3" in messages[0]


def test_it_still_decodes_valid_actions_and_logs_nothing(decode_context, caplog):
    preserve = _action(TriggerActionId.PRESERVE_TRIGGER)
    with caplog.at_level(logging.ERROR):
        result = RichChkTrigTranscoder()._decode_single_action(
            preserve, decode_context, 0
        )
    assert isinstance(result, PreserveTrigger)
    assert not [r for r in caplog.records if "Failed to decode" in r.getMessage()]


def test_it_only_falls_back_for_the_bad_action_and_keeps_the_rest_of_the_trigger_rich(
    junk_doodad_action, junk_deaths_condition, decode_context
):
    preserve = _action(TriggerActionId.PRESERVE_TRIGGER)
    trigger = RichChkTrigTranscoder()._decode_trigger(
        _trigger([junk_deaths_condition], [junk_doodad_action, preserve]),
        decode_context,
        0,
    )
    assert trigger.conditions == [junk_deaths_condition]
    assert trigger.actions[0] is junk_doodad_action
    assert isinstance(trigger.actions[1], PreserveTrigger)
    assert not isinstance(trigger.actions[0], SetDoodadStateAction)
    assert not isinstance(trigger.conditions[0], DeathsCondition)


def test_it_writes_the_raw_action_and_condition_back_unchanged(
    junk_doodad_action, junk_deaths_condition, decode_context, encode_context
):
    transcoder = RichChkTrigTranscoder()
    decoded = _trigger(
        [junk_deaths_condition],
        [junk_doodad_action, _action(TriggerActionId.PRESERVE_TRIGGER)],
    )
    rich = transcoder._decode_trigger(decoded, decode_context, 0)
    encoded = transcoder._encode_trigger(rich, encode_context)
    assert encoded.conditions[0] == junk_deaths_condition
    assert encoded.actions[0] == junk_doodad_action
