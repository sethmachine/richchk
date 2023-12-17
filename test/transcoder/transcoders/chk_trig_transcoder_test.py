from chkjson.model.chk.trig.decoded_action import DecodedAction
from chkjson.model.chk.trig.decoded_condition import DecodedCondition
from chkjson.model.chk.trig.decoded_player_execution import DecodedPlayerExecution
from chkjson.model.chk.trig.decoded_trig_section import DecodedTrigSection
from chkjson.model.chk.trig.decoded_trigger import DecodedTrigger
from chkjson.transcoder.chk.transcoders.chk_trig_transcoder import ChkTrigTranscoder

from ...chk_resources import CHK_SECTION_FILE_PATHS

# these are the default triggers in melee/SCM maps
# CONDITION: always ACTION: modify resources for current player set to 50 minerals
_ALL_PLAYERS_EXECUTION = [0] * 17 + [1] + [0] * 9
_EXPECTED_STARTING_RESOURCES_TRIGGER = DecodedTrigger(
    _conditions=[
        DecodedCondition(
            _location_id=0,
            _group=0,
            _quantity=0,
            _unit_id=0,
            _numeric_comparison_operation=0,
            _condition_id=22,
            _numeric_comparand_type=0,
            _flags=0,
            _mask_flag=0,
        )
    ],
    _actions=[
        DecodedAction(
            _location_id=0,
            _text_string_id=0,
            _wav_string_id=0,
            _time=0,
            _first_group=13,
            _second_group=50,
            _action_argument_type=0,
            _action_id=26,
            _quantifier_or_switch_or_order=7,
            _flags=0,
            _padding=0,
            _mask_flag=0,
        )
    ],
    _player_execution=DecodedPlayerExecution(0, _ALL_PLAYERS_EXECUTION, 0),
)
# CONDITION: current player commands 0 buildings ACTION: defeat
_EXPECTED_DEFEAT_TRIGGER = DecodedTrigger(
    _conditions=[
        DecodedCondition(
            _location_id=0,
            _group=13,
            _quantity=0,
            _unit_id=231,
            _numeric_comparison_operation=1,
            _condition_id=2,
            _numeric_comparand_type=0,
            _flags=0,
            _mask_flag=0,
        )
    ],
    _actions=[
        DecodedAction(
            _location_id=0,
            _text_string_id=0,
            _wav_string_id=0,
            _time=0,
            _first_group=0,
            _second_group=0,
            _action_argument_type=0,
            _action_id=2,
            _quantifier_or_switch_or_order=0,
            _flags=0,
            _padding=0,
            _mask_flag=0,
        )
    ],
    _player_execution=DecodedPlayerExecution(0, _ALL_PLAYERS_EXECUTION, 0),
)

# CONDITION: non-allied victory players commands at most 0 buildings ACTION: victory
_EXPECTED_VICTORY_TRIGGER = DecodedTrigger(
    _conditions=[
        DecodedCondition(
            _location_id=0,
            _group=26,
            _quantity=0,
            _unit_id=231,
            _numeric_comparison_operation=1,
            _condition_id=2,
            _numeric_comparand_type=0,
            _flags=0,
            _mask_flag=0,
        )
    ],
    _actions=[
        DecodedAction(
            _location_id=0,
            _text_string_id=0,
            _wav_string_id=0,
            _time=0,
            _first_group=0,
            _second_group=0,
            _action_argument_type=0,
            _action_id=1,
            _quantifier_or_switch_or_order=0,
            _flags=0,
            _padding=0,
            _mask_flag=0,
        )
    ],
    _player_execution=DecodedPlayerExecution(0, _ALL_PLAYERS_EXECUTION, 0),
)


def _read_chk_section() -> bytes:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedTrigSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return chk_binary_data


def test_it_decodes_expected_triggers():
    transcoder: ChkTrigTranscoder = ChkTrigTranscoder()
    chk_binary_data = _read_chk_section()
    trig_section: DecodedTrigSection = transcoder.decode(chk_binary_data)
    triggers = trig_section.triggers
    assert len(triggers) == 3
    resources_trigger = triggers[0]
    assert (
        _EXPECTED_STARTING_RESOURCES_TRIGGER.conditions[0]
        in resources_trigger.conditions
    )
    assert _EXPECTED_STARTING_RESOURCES_TRIGGER.actions[0] in resources_trigger.actions
    assert (
        _EXPECTED_STARTING_RESOURCES_TRIGGER.player_execution
        == resources_trigger.player_execution
    )
    defeat_trigger = triggers[1]
    assert _EXPECTED_DEFEAT_TRIGGER.conditions[0] in defeat_trigger.conditions
    assert _EXPECTED_DEFEAT_TRIGGER.actions[0] in defeat_trigger.actions
    assert _EXPECTED_DEFEAT_TRIGGER.player_execution == defeat_trigger.player_execution
    victory_trigger = triggers[2]
    assert _EXPECTED_VICTORY_TRIGGER.conditions[0] in victory_trigger.conditions
    assert _EXPECTED_VICTORY_TRIGGER.actions[0] in victory_trigger.actions
    assert (
        _EXPECTED_VICTORY_TRIGGER.player_execution == victory_trigger.player_execution
    )


def test_it_decodes_and_encodes_without_changing_data():
    transcoder: ChkTrigTranscoder = ChkTrigTranscoder()
    chk_binary_data = _read_chk_section()
    trig_section: DecodedTrigSection = transcoder.decode(chk_binary_data)
    actual_encoded_data = transcoder.encode(trig_section, include_header=False)
    assert actual_encoded_data == chk_binary_data
    assert transcoder.decode(actual_encoded_data) == transcoder.decode(chk_binary_data)
