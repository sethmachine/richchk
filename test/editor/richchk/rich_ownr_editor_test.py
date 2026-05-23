import pytest

from richchk.editor.richchk.rich_ownr_editor import RichOwnrEditor
from richchk.model.richchk.ownr.player_type import PlayerType
from richchk.model.richchk.ownr.rich_ownr_section import RichOwnrSection
from richchk.model.richchk.trig.player_id import PlayerId

_NUM_PLAYERS = 12
_ALL_INACTIVE = [PlayerType.INACTIVE] * _NUM_PLAYERS


@pytest.fixture
def inactive_ownr() -> RichOwnrSection:
    return RichOwnrSection(_player_types=list(_ALL_INACTIVE))


def test_it_sets_single_player_type(inactive_ownr):
    editor = RichOwnrEditor()
    updated = editor.set_player_type(PlayerId.PLAYER_1, PlayerType.HUMAN, inactive_ownr)
    assert updated.player_types[0] == PlayerType.HUMAN
    assert updated.player_types[1:] == list(_ALL_INACTIVE)[1:]


def test_it_does_not_mutate_original_section(inactive_ownr):
    editor = RichOwnrEditor()
    editor.set_player_type(PlayerId.PLAYER_1, PlayerType.HUMAN, inactive_ownr)
    assert inactive_ownr.player_types[0] == PlayerType.INACTIVE


def test_it_sets_all_player_types(inactive_ownr):
    editor = RichOwnrEditor()
    new_types = {
        PlayerId.PLAYER_1: PlayerType.HUMAN,
        PlayerId.PLAYER_2: PlayerType.HUMAN,
        PlayerId.PLAYER_3: PlayerType.COMPUTER,
        PlayerId.PLAYER_4: PlayerType.COMPUTER,
        PlayerId.PLAYER_5: PlayerType.RESCUE_PASSIVE,
        PlayerId.PLAYER_6: PlayerType.NEUTRAL,
        PlayerId.PLAYER_7: PlayerType.INACTIVE,
        PlayerId.PLAYER_8: PlayerType.INACTIVE,
        PlayerId.PLAYER_9: PlayerType.INACTIVE,
        PlayerId.PLAYER_10: PlayerType.INACTIVE,
        PlayerId.PLAYER_11: PlayerType.INACTIVE,
        PlayerId.PLAYER_12: PlayerType.INACTIVE,
    }
    updated = editor.set_all_player_types(new_types, inactive_ownr)
    assert updated.player_types == list(new_types.values())


def test_it_raises_on_invalid_player_slot(inactive_ownr):
    editor = RichOwnrEditor()
    with pytest.raises(ValueError):
        editor.set_player_type(PlayerId.NONE, PlayerType.HUMAN, inactive_ownr)


def test_it_defaults_missing_slots_to_inactive(inactive_ownr):
    editor = RichOwnrEditor()
    updated = editor.set_all_player_types(
        {PlayerId.PLAYER_1: PlayerType.HUMAN},
        inactive_ownr,
    )
    assert updated.player_types[0] == PlayerType.HUMAN
    assert all(t == PlayerType.CLOSED for t in updated.player_types[1:])
