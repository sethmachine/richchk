import pytest

from richchk.editor.richchk.rich_side_editor import RichSideEditor
from richchk.model.richchk.side.player_race import PlayerRace
from richchk.model.richchk.side.rich_side_section import RichSideSection

_NUM_PLAYERS = 12
_ALL_INACTIVE = [PlayerRace.INACTIVE] * _NUM_PLAYERS


@pytest.fixture
def inactive_side() -> RichSideSection:
    return RichSideSection(_player_races=list(_ALL_INACTIVE))


def test_it_sets_single_player_race(inactive_side):
    editor = RichSideEditor()
    updated = editor.set_player_race(0, PlayerRace.TERRAN, inactive_side)
    assert updated.player_races[0] == PlayerRace.TERRAN
    assert updated.player_races[1:] == list(_ALL_INACTIVE)[1:]


def test_it_does_not_mutate_original_section(inactive_side):
    editor = RichSideEditor()
    editor.set_player_race(0, PlayerRace.TERRAN, inactive_side)
    assert inactive_side.player_races[0] == PlayerRace.INACTIVE


def test_it_sets_all_player_races(inactive_side):
    editor = RichSideEditor()
    new_races = [
        PlayerRace.TERRAN,
        PlayerRace.ZERG,
        PlayerRace.PROTOSS,
        PlayerRace.RANDOM,
        PlayerRace.INACTIVE,
        PlayerRace.INACTIVE,
        PlayerRace.INACTIVE,
        PlayerRace.INACTIVE,
        PlayerRace.INACTIVE,
        PlayerRace.INACTIVE,
        PlayerRace.INACTIVE,
        PlayerRace.INACTIVE,
    ]
    updated = editor.set_all_player_races(new_races, inactive_side)
    assert updated.player_races == new_races


def test_it_raises_on_invalid_player_slot(inactive_side):
    editor = RichSideEditor()
    with pytest.raises(ValueError):
        editor.set_player_race(-1, PlayerRace.TERRAN, inactive_side)
    with pytest.raises(ValueError):
        editor.set_player_race(12, PlayerRace.TERRAN, inactive_side)


def test_it_raises_on_wrong_race_count(inactive_side):
    editor = RichSideEditor()
    with pytest.raises(ValueError):
        editor.set_all_player_races([PlayerRace.TERRAN] * 8, inactive_side)
