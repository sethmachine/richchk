import pytest

from richchk.editor.richchk.rich_ownr_editor import RichOwnrEditor
from richchk.model.richchk.ownr.player_controller import PlayerController
from richchk.model.richchk.ownr.rich_ownr_section import RichOwnrSection

_NUM_PLAYERS = 12
_ALL_INACTIVE = [PlayerController.INACTIVE] * _NUM_PLAYERS


@pytest.fixture
def inactive_ownr() -> RichOwnrSection:
    return RichOwnrSection(_player_controllers=list(_ALL_INACTIVE))


def test_it_sets_single_player_controller(inactive_ownr):
    editor = RichOwnrEditor()
    updated = editor.set_player_controller(0, PlayerController.HUMAN, inactive_ownr)
    assert updated.player_controllers[0] == PlayerController.HUMAN
    assert updated.player_controllers[1:] == list(_ALL_INACTIVE)[1:]


def test_it_does_not_mutate_original_section(inactive_ownr):
    editor = RichOwnrEditor()
    editor.set_player_controller(0, PlayerController.HUMAN, inactive_ownr)
    assert inactive_ownr.player_controllers[0] == PlayerController.INACTIVE


def test_it_sets_all_player_controllers(inactive_ownr):
    editor = RichOwnrEditor()
    new_controllers = [
        PlayerController.HUMAN,
        PlayerController.HUMAN,
        PlayerController.COMPUTER,
        PlayerController.COMPUTER,
        PlayerController.RESCUE_PASSIVE,
        PlayerController.NEUTRAL,
        PlayerController.INACTIVE,
        PlayerController.INACTIVE,
        PlayerController.INACTIVE,
        PlayerController.INACTIVE,
        PlayerController.INACTIVE,
        PlayerController.INACTIVE,
    ]
    updated = editor.set_all_player_controllers(new_controllers, inactive_ownr)
    assert updated.player_controllers == new_controllers


def test_it_raises_on_invalid_player_slot(inactive_ownr):
    editor = RichOwnrEditor()
    with pytest.raises(ValueError):
        editor.set_player_controller(-1, PlayerController.HUMAN, inactive_ownr)
    with pytest.raises(ValueError):
        editor.set_player_controller(12, PlayerController.HUMAN, inactive_ownr)


def test_it_raises_on_wrong_controller_count(inactive_ownr):
    editor = RichOwnrEditor()
    with pytest.raises(ValueError):
        editor.set_all_player_controllers([PlayerController.HUMAN] * 8, inactive_ownr)
