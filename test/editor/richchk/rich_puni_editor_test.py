import pytest

from richchk.editor.richchk.rich_puni_editor import RichPuniEditor
from richchk.model.richchk.puni.rich_puni_section import RichPuniSection
from richchk.model.richchk.trig.player_id import PlayerId
from richchk.model.richchk.unis.unit_id import UnitId

_GAME_PLAYERS = [p for p in PlayerId if p.id < 12]
_GAME_UNITS = [u for u in UnitId if u.id < 228]


def _make_puni(
    player_availability: bool = True,
    global_availability: bool = True,
    player_defaults: bool = True,
) -> RichPuniSection:
    return RichPuniSection(
        _player_unit_availability={
            p: {u: player_availability for u in _GAME_UNITS} for p in _GAME_PLAYERS
        },
        _global_unit_availability={u: global_availability for u in _GAME_UNITS},
        _player_uses_defaults={
            p: {u: player_defaults for u in _GAME_UNITS} for p in _GAME_PLAYERS
        },
    )


@pytest.fixture
def default_puni() -> RichPuniSection:
    return _make_puni()


def test_it_sets_unit_available_for_player(default_puni):
    editor = RichPuniEditor()
    updated = editor.set_unit_available_for_player(
        PlayerId.PLAYER_1, UnitId.TERRAN_MARINE, False, default_puni
    )
    assert (
        updated.player_unit_availability[PlayerId.PLAYER_1][UnitId.TERRAN_MARINE]
        is False
    )
    assert (
        updated.player_unit_availability[PlayerId.PLAYER_1][UnitId.TERRAN_GHOST] is True
    )


def test_it_sets_uses_defaults_false_on_player_availability_override(default_puni):
    editor = RichPuniEditor()
    updated = editor.set_unit_available_for_player(
        PlayerId.PLAYER_1, UnitId.TERRAN_MARINE, False, default_puni
    )
    assert (
        updated.player_uses_defaults[PlayerId.PLAYER_1][UnitId.TERRAN_MARINE] is False
    )
    assert updated.player_uses_defaults[PlayerId.PLAYER_1][UnitId.TERRAN_GHOST] is True


def test_it_does_not_mutate_original_on_player_availability(default_puni):
    editor = RichPuniEditor()
    editor.set_unit_available_for_player(
        PlayerId.PLAYER_1, UnitId.TERRAN_MARINE, False, default_puni
    )
    assert (
        default_puni.player_unit_availability[PlayerId.PLAYER_1][UnitId.TERRAN_MARINE]
        is True
    )
    assert (
        default_puni.player_uses_defaults[PlayerId.PLAYER_1][UnitId.TERRAN_MARINE]
        is True
    )


def test_it_sets_player_uses_default(default_puni):
    editor = RichPuniEditor()
    updated = editor.set_player_uses_default(
        PlayerId.PLAYER_2, UnitId.TERRAN_GHOST, False, default_puni
    )
    assert updated.player_uses_defaults[PlayerId.PLAYER_2][UnitId.TERRAN_GHOST] is False
    assert updated.player_uses_defaults[PlayerId.PLAYER_1][UnitId.TERRAN_MARINE] is True


def test_it_does_not_mutate_original_on_player_defaults(default_puni):
    editor = RichPuniEditor()
    editor.set_player_uses_default(
        PlayerId.PLAYER_1, UnitId.TERRAN_MARINE, False, default_puni
    )
    assert (
        default_puni.player_uses_defaults[PlayerId.PLAYER_1][UnitId.TERRAN_MARINE]
        is True
    )


def test_it_sets_unit_global_availability(default_puni):
    editor = RichPuniEditor()
    updated = editor.set_unit_global_availability(
        UnitId.TERRAN_MARINE, False, default_puni
    )
    assert updated.global_unit_availability[UnitId.TERRAN_MARINE] is False
    assert updated.global_unit_availability[UnitId.TERRAN_GHOST] is True


def test_it_preserves_other_players_on_availability_update(default_puni):
    editor = RichPuniEditor()
    updated = editor.set_unit_available_for_player(
        PlayerId.PLAYER_1, UnitId.TERRAN_MARINE, False, default_puni
    )
    for player in _GAME_PLAYERS:
        if player == PlayerId.PLAYER_1:
            continue
        assert all(updated.player_unit_availability[player].values())


def test_apply_player_unit_availability_merges_partial_dict(default_puni):
    editor = RichPuniEditor()
    updates = {
        PlayerId.PLAYER_1: {UnitId.TERRAN_MARINE: False, UnitId.TERRAN_GHOST: False},
        PlayerId.PLAYER_2: {UnitId.PROTOSS_ZEALOT: False},
    }
    updated = editor.apply_player_unit_availability(updates, default_puni)
    assert (
        updated.player_unit_availability[PlayerId.PLAYER_1][UnitId.TERRAN_MARINE]
        is False
    )
    assert (
        updated.player_unit_availability[PlayerId.PLAYER_1][UnitId.TERRAN_GHOST]
        is False
    )
    assert (
        updated.player_unit_availability[PlayerId.PLAYER_2][UnitId.PROTOSS_ZEALOT]
        is False
    )
    assert (
        updated.player_unit_availability[PlayerId.PLAYER_1][UnitId.ZERG_ZERGLING]
        is True
    )
    assert (
        updated.player_unit_availability[PlayerId.PLAYER_3][UnitId.TERRAN_MARINE]
        is True
    )


def test_apply_player_unit_availability_sets_uses_defaults_false(default_puni):
    editor = RichPuniEditor()
    updates = {PlayerId.PLAYER_1: {UnitId.TERRAN_MARINE: False}}
    updated = editor.apply_player_unit_availability(updates, default_puni)
    assert (
        updated.player_uses_defaults[PlayerId.PLAYER_1][UnitId.TERRAN_MARINE] is False
    )
    assert updated.player_uses_defaults[PlayerId.PLAYER_1][UnitId.TERRAN_GHOST] is True


def test_apply_player_unit_availability_does_not_mutate_original(default_puni):
    editor = RichPuniEditor()
    updates = {PlayerId.PLAYER_1: {UnitId.TERRAN_MARINE: False}}
    editor.apply_player_unit_availability(updates, default_puni)
    assert (
        default_puni.player_unit_availability[PlayerId.PLAYER_1][UnitId.TERRAN_MARINE]
        is True
    )
    assert (
        default_puni.player_uses_defaults[PlayerId.PLAYER_1][UnitId.TERRAN_MARINE]
        is True
    )
