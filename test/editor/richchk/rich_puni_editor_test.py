import pytest

from richchk.editor.richchk.rich_puni_editor import RichPuniEditor
from richchk.model.richchk.puni.rich_puni_section import RichPuniSection
from richchk.model.richchk.trig.player_id import PlayerId
from richchk.model.richchk.unis.unit_id import UnitId

_NUM_PLAYERS = 12
_NUM_UNITS = 228


def _make_puni(
    player_availability: bool = True,
    global_availability: bool = True,
    player_defaults: bool = True,
) -> RichPuniSection:
    return RichPuniSection(
        _player_unit_availability=[
            [player_availability] * _NUM_UNITS for _ in range(_NUM_PLAYERS)
        ],
        _global_unit_availability=[global_availability] * _NUM_UNITS,
        _player_uses_defaults=[
            [player_defaults] * _NUM_UNITS for _ in range(_NUM_PLAYERS)
        ],
    )


@pytest.fixture
def default_puni() -> RichPuniSection:
    return _make_puni()


def test_it_sets_unit_available_for_player(default_puni):
    editor = RichPuniEditor()
    updated = editor.set_unit_available_for_player(
        PlayerId.PLAYER_1, UnitId.TERRAN_MARINE, False, default_puni
    )
    assert updated.player_unit_availability[0][0] is False
    assert updated.player_unit_availability[0][1] is True


def test_it_does_not_mutate_original_on_player_availability(default_puni):
    editor = RichPuniEditor()
    editor.set_unit_available_for_player(
        PlayerId.PLAYER_1, UnitId.TERRAN_MARINE, False, default_puni
    )
    assert default_puni.player_unit_availability[0][0] is True


def test_it_sets_player_uses_default(default_puni):
    editor = RichPuniEditor()
    updated = editor.set_player_uses_default(
        PlayerId.PLAYER_2, UnitId.TERRAN_GHOST, False, default_puni
    )
    assert updated.player_uses_defaults[1][1] is False
    assert updated.player_uses_defaults[0][0] is True


def test_it_does_not_mutate_original_on_player_defaults(default_puni):
    editor = RichPuniEditor()
    editor.set_player_uses_default(
        PlayerId.PLAYER_1, UnitId.TERRAN_MARINE, False, default_puni
    )
    assert default_puni.player_uses_defaults[0][0] is True


def test_it_sets_unit_global_availability(default_puni):
    editor = RichPuniEditor()
    updated = editor.set_unit_global_availability(
        UnitId.TERRAN_MARINE, False, default_puni
    )
    assert updated.global_unit_availability[0] is False
    assert updated.global_unit_availability[1] is True


def test_it_preserves_other_players_on_availability_update(default_puni):
    editor = RichPuniEditor()
    updated = editor.set_unit_available_for_player(
        PlayerId.PLAYER_1, UnitId.TERRAN_MARINE, False, default_puni
    )
    for p in range(1, _NUM_PLAYERS):
        assert all(updated.player_unit_availability[p])
