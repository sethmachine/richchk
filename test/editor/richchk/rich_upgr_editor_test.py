import pytest

from richchk.editor.richchk.rich_upgr_editor import RichUpgrEditor
from richchk.model.richchk.trig.player_id import PlayerId
from richchk.model.richchk.upgr.rich_upgr_section import RichUpgrSection
from richchk.model.richchk.upgrades.upgrade_id import UpgradeId

_GAME_PLAYERS = [p for p in PlayerId if p.id < 12]
_CLASSIC_UPGRADES = [u for u in UpgradeId if u.id < 46]


def _make_upgr(
    player_max: int = 3,
    player_start: int = 0,
    global_max: int = 3,
    global_start: int = 0,
    player_defaults: bool = True,
) -> RichUpgrSection:
    return RichUpgrSection(
        _player_max_levels={
            p: {u: player_max for u in _CLASSIC_UPGRADES} for p in _GAME_PLAYERS
        },
        _player_start_levels={
            p: {u: player_start for u in _CLASSIC_UPGRADES} for p in _GAME_PLAYERS
        },
        _global_max_levels={u: global_max for u in _CLASSIC_UPGRADES},
        _global_start_levels={u: global_start for u in _CLASSIC_UPGRADES},
        _player_uses_defaults={
            p: {u: player_defaults for u in _CLASSIC_UPGRADES} for p in _GAME_PLAYERS
        },
    )


@pytest.fixture
def default_upgr() -> RichUpgrSection:
    return _make_upgr()


def test_it_sets_player_max_level(default_upgr):
    editor = RichUpgrEditor()
    updated = editor.set_player_max_level(
        PlayerId.PLAYER_1, UpgradeId.TERRAN_INFANTRY_ARMOR, 2, default_upgr
    )
    assert (
        updated.player_max_levels[PlayerId.PLAYER_1][UpgradeId.TERRAN_INFANTRY_ARMOR]
        == 2
    )
    assert (
        updated.player_max_levels[PlayerId.PLAYER_1][UpgradeId.TERRAN_VEHICLE_PLATING]
        == 3
    )


def test_it_does_not_mutate_original_on_max_level(default_upgr):
    editor = RichUpgrEditor()
    editor.set_player_max_level(
        PlayerId.PLAYER_1, UpgradeId.TERRAN_INFANTRY_ARMOR, 2, default_upgr
    )
    assert (
        default_upgr.player_max_levels[PlayerId.PLAYER_1][
            UpgradeId.TERRAN_INFANTRY_ARMOR
        ]
        == 3
    )


def test_it_sets_player_start_level(default_upgr):
    editor = RichUpgrEditor()
    updated = editor.set_player_start_level(
        PlayerId.PLAYER_2, UpgradeId.TERRAN_VEHICLE_PLATING, 1, default_upgr
    )
    assert (
        updated.player_start_levels[PlayerId.PLAYER_2][UpgradeId.TERRAN_VEHICLE_PLATING]
        == 1
    )
    assert (
        updated.player_start_levels[PlayerId.PLAYER_1][UpgradeId.TERRAN_INFANTRY_ARMOR]
        == 0
    )


def test_it_sets_player_uses_default(default_upgr):
    editor = RichUpgrEditor()
    updated = editor.set_player_uses_default(
        PlayerId.PLAYER_1, UpgradeId.TERRAN_INFANTRY_ARMOR, False, default_upgr
    )
    assert (
        updated.player_uses_defaults[PlayerId.PLAYER_1][UpgradeId.TERRAN_INFANTRY_ARMOR]
        is False
    )
    assert (
        updated.player_uses_defaults[PlayerId.PLAYER_1][
            UpgradeId.TERRAN_VEHICLE_PLATING
        ]
        is True
    )


def test_it_sets_uses_defaults_false_on_max_level_override(default_upgr):
    editor = RichUpgrEditor()
    updated = editor.set_player_max_level(
        PlayerId.PLAYER_1, UpgradeId.TERRAN_INFANTRY_ARMOR, 2, default_upgr
    )
    assert (
        updated.player_uses_defaults[PlayerId.PLAYER_1][UpgradeId.TERRAN_INFANTRY_ARMOR]
        is False
    )
    assert (
        updated.player_uses_defaults[PlayerId.PLAYER_1][
            UpgradeId.TERRAN_VEHICLE_PLATING
        ]
        is True
    )


def test_it_sets_uses_defaults_false_on_start_level_override(default_upgr):
    editor = RichUpgrEditor()
    updated = editor.set_player_start_level(
        PlayerId.PLAYER_1, UpgradeId.TERRAN_INFANTRY_ARMOR, 1, default_upgr
    )
    assert (
        updated.player_uses_defaults[PlayerId.PLAYER_1][UpgradeId.TERRAN_INFANTRY_ARMOR]
        is False
    )
    assert (
        updated.player_uses_defaults[PlayerId.PLAYER_1][
            UpgradeId.TERRAN_VEHICLE_PLATING
        ]
        is True
    )


def test_it_preserves_other_players_on_max_level_update(default_upgr):
    editor = RichUpgrEditor()
    updated = editor.set_player_max_level(
        PlayerId.PLAYER_1, UpgradeId.TERRAN_INFANTRY_ARMOR, 0, default_upgr
    )
    for player in _GAME_PLAYERS:
        if player == PlayerId.PLAYER_1:
            continue
        assert all(v == 3 for v in updated.player_max_levels[player].values())


def test_apply_player_max_levels_merges_partial_dict(default_upgr):
    editor = RichUpgrEditor()
    updates = {
        PlayerId.PLAYER_1: {
            UpgradeId.TERRAN_INFANTRY_ARMOR: 1,
            UpgradeId.TERRAN_VEHICLE_PLATING: 2,
        },
        PlayerId.PLAYER_2: {UpgradeId.TERRAN_INFANTRY_ARMOR: 0},
    }
    updated = editor.apply_player_max_levels(updates, default_upgr)
    assert (
        updated.player_max_levels[PlayerId.PLAYER_1][UpgradeId.TERRAN_INFANTRY_ARMOR]
        == 1
    )
    assert (
        updated.player_max_levels[PlayerId.PLAYER_1][UpgradeId.TERRAN_VEHICLE_PLATING]
        == 2
    )
    assert (
        updated.player_max_levels[PlayerId.PLAYER_2][UpgradeId.TERRAN_INFANTRY_ARMOR]
        == 0
    )
    assert updated.player_max_levels[PlayerId.PLAYER_1][UpgradeId.ZERG_CARAPACE] == 3
    assert (
        updated.player_max_levels[PlayerId.PLAYER_3][UpgradeId.TERRAN_INFANTRY_ARMOR]
        == 3
    )
    assert (
        updated.player_uses_defaults[PlayerId.PLAYER_1][UpgradeId.TERRAN_INFANTRY_ARMOR]
        is False
    )
    assert (
        updated.player_uses_defaults[PlayerId.PLAYER_1][UpgradeId.ZERG_CARAPACE] is True
    )


def test_apply_player_start_levels_merges_partial_dict(default_upgr):
    editor = RichUpgrEditor()
    updates = {
        PlayerId.PLAYER_1: {UpgradeId.TERRAN_INFANTRY_ARMOR: 1},
        PlayerId.PLAYER_2: {UpgradeId.TERRAN_VEHICLE_PLATING: 2},
    }
    updated = editor.apply_player_start_levels(updates, default_upgr)
    assert (
        updated.player_start_levels[PlayerId.PLAYER_1][UpgradeId.TERRAN_INFANTRY_ARMOR]
        == 1
    )
    assert (
        updated.player_start_levels[PlayerId.PLAYER_2][UpgradeId.TERRAN_VEHICLE_PLATING]
        == 2
    )
    assert updated.player_start_levels[PlayerId.PLAYER_1][UpgradeId.ZERG_CARAPACE] == 0
    assert (
        updated.player_uses_defaults[PlayerId.PLAYER_1][UpgradeId.TERRAN_INFANTRY_ARMOR]
        is False
    )
    assert (
        updated.player_uses_defaults[PlayerId.PLAYER_1][UpgradeId.ZERG_CARAPACE] is True
    )
