""""""


import pytest

from richchk.editor.richchk.rich_trig_editor import RichTrigEditor
from richchk.model.richchk.str.rich_string import RichString
from richchk.model.richchk.trig.actions.display_text_message_action import (
    DisplayTextMessageAction,
)
from richchk.model.richchk.trig.conditions.always_condition import AlwaysCondition
from richchk.model.richchk.trig.player_id import PlayerId
from richchk.model.richchk.trig.rich_trig_section import RichTrigSection
from richchk.model.richchk.trig.rich_trigger import RichTrigger


@pytest.fixture(scope="function")
def example_trigger():
    return RichTrigger(
        _conditions=[AlwaysCondition()],
        _actions=[DisplayTextMessageAction(_text=RichString(_value="Hello world!"))],
        _players={PlayerId.ALL_PLAYERS},
    )


@pytest.fixture(scope="function")
def rich_trig(example_trigger):
    return RichTrigSection(_triggers=[example_trigger])


def test_it_adds_triggers(rich_trig):
    new_triggers = [
        RichTrigger(
            _conditions=[AlwaysCondition()],
            _actions=[
                DisplayTextMessageAction(_text=RichString(_value="Hello Player 2"))
            ],
            _players={PlayerId.PLAYER_2},
        ),
        RichTrigger(
            _conditions=[AlwaysCondition()],
            _actions=[
                DisplayTextMessageAction(_text=RichString(_value="Hello Player 1"))
            ],
            _players={PlayerId.PLAYER_1},
        ),
    ]
    expected_triggers = rich_trig.triggers + new_triggers
    new_trig = RichTrigEditor.add_triggers(new_triggers, rich_trig)
    assert len(new_trig.triggers) == len(expected_triggers)
    for expected in expected_triggers:
        assert expected in new_trig.triggers
