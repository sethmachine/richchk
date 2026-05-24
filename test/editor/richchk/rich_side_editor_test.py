import pytest

from richchk.editor.richchk.rich_side_editor import RichSideEditor
from richchk.model.richchk.side.player_race import PlayerRace
from richchk.model.richchk.side.rich_side_section import RichSideSection
from richchk.model.richchk.trig.player_id import PlayerId

_NUM_PLAYERS = 12
_ALL_INACTIVE = [PlayerRace.INACTIVE] * _NUM_PLAYERS


@pytest.fixture
def inactive_side() -> RichSideSection:
    return RichSideSection(_player_races=list(_ALL_INACTIVE))


def test_it_sets_single_player_race(inactive_side):
    editor = RichSideEditor()
    updated = editor.set_player_race(
        PlayerId.PLAYER_1, PlayerRace.TERRAN, inactive_side
    )
    assert updated.player_races[0] == PlayerRace.TERRAN
    assert updated.player_races[1:] == list(_ALL_INACTIVE)[1:]


def test_it_does_not_mutate_original_section(inactive_side):
    editor = RichSideEditor()
    editor.set_player_race(PlayerId.PLAYER_1, PlayerRace.TERRAN, inactive_side)
    assert inactive_side.player_races[0] == PlayerRace.INACTIVE


def test_it_sets_all_player_races(inactive_side):
    editor = RichSideEditor()
    updates = {
        PlayerId.PLAYER_1: PlayerRace.TERRAN,
        PlayerId.PLAYER_2: PlayerRace.ZERG,
        PlayerId.PLAYER_3: PlayerRace.PROTOSS,
        PlayerId.PLAYER_4: PlayerRace.RANDOM,
    }
    updated = editor.set_player_races(updates, inactive_side)
    assert updated.player_races[0] == PlayerRace.TERRAN
    assert updated.player_races[1] == PlayerRace.ZERG
    assert updated.player_races[2] == PlayerRace.PROTOSS
    assert updated.player_races[3] == PlayerRace.RANDOM
    assert all(r == PlayerRace.INACTIVE for r in updated.player_races[4:])


def test_it_preserves_unspecified_slots(inactive_side):
    editor = RichSideEditor()
    updated = editor.set_player_races(
        {PlayerId.PLAYER_1: PlayerRace.TERRAN},
        inactive_side,
    )
    assert updated.player_races[0] == PlayerRace.TERRAN
    assert all(r == PlayerRace.INACTIVE for r in updated.player_races[1:])


def test_it_raises_on_invalid_player_slot(inactive_side):
    editor = RichSideEditor()
    with pytest.raises(ValueError):
        editor.set_player_race(PlayerId.NONE, PlayerRace.TERRAN, inactive_side)
