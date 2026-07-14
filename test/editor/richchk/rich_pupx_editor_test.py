import pytest

from richchk.editor.richchk.rich_pupx_editor import RichPupxEditor
from richchk.model.richchk.pupx.rich_pupx_section import RichPupxSection
from richchk.model.richchk.trig.player_id import PlayerId
from richchk.model.richchk.upgrades.upgrade_id import UpgradeId

_GAME_PLAYERS = [p for p in PlayerId if p.id < 12]
_BW_UPGRADES = list(UpgradeId)


def _make_pupx(
    player_max: int = 3,
    player_start: int = 0,
    global_max: int = 3,
    global_start: int = 0,
    player_defaults: bool = True,
) -> RichPupxSection:
    return RichPupxSection(
        _player_max_levels={
            p: {u: player_max for u in _BW_UPGRADES} for p in _GAME_PLAYERS
        },
        _player_start_levels={
            p: {u: player_start for u in _BW_UPGRADES} for p in _GAME_PLAYERS
        },
        _global_max_levels={u: global_max for u in _BW_UPGRADES},
        _global_start_levels={u: global_start for u in _BW_UPGRADES},
        _player_uses_defaults={
            p: {u: player_defaults for u in _BW_UPGRADES} for p in _GAME_PLAYERS
        },
    )


@pytest.fixture
def default_pupx() -> RichPupxSection:
    return _make_pupx()


def test_it_sets_player_max_level(default_pupx):
    editor = RichPupxEditor()
    updated = editor.set_player_max_level(
        PlayerId.PLAYER_1, UpgradeId.TERRAN_INFANTRY_ARMOR, 2, default_pupx
    )
    assert (
        updated.player_max_levels[PlayerId.PLAYER_1][UpgradeId.TERRAN_INFANTRY_ARMOR]
        == 2
    )
    assert (
        updated.player_max_levels[PlayerId.PLAYER_1][UpgradeId.TERRAN_VEHICLE_PLATING]
        == 3
    )


def test_it_does_not_mutate_original_on_max_level(default_pupx):
    editor = RichPupxEditor()
    editor.set_player_max_level(
        PlayerId.PLAYER_1, UpgradeId.TERRAN_INFANTRY_ARMOR, 2, default_pupx
    )
    assert (
        default_pupx.player_max_levels[PlayerId.PLAYER_1][
            UpgradeId.TERRAN_INFANTRY_ARMOR
        ]
        == 3
    )


def test_it_sets_player_start_level(default_pupx):
    editor = RichPupxEditor()
    updated = editor.set_player_start_level(
        PlayerId.PLAYER_2, UpgradeId.TERRAN_VEHICLE_PLATING, 1, default_pupx
    )
    assert (
        updated.player_start_levels[PlayerId.PLAYER_2][UpgradeId.TERRAN_VEHICLE_PLATING]
        == 1
    )
    assert (
        updated.player_start_levels[PlayerId.PLAYER_1][UpgradeId.TERRAN_INFANTRY_ARMOR]
        == 0
    )


def test_it_sets_player_uses_default(default_pupx):
    editor = RichPupxEditor()
    updated = editor.set_player_uses_default(
        PlayerId.PLAYER_1, UpgradeId.TERRAN_INFANTRY_ARMOR, False, default_pupx
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


def test_it_allows_upgrade_id_60_bw_only(default_pupx):
    editor = RichPupxEditor()
    updated = editor.set_player_max_level(
        PlayerId.PLAYER_1, UpgradeId.UNKNOWN_UPGRADE_60, 2, default_pupx
    )
    assert (
        updated.player_max_levels[PlayerId.PLAYER_1][UpgradeId.UNKNOWN_UPGRADE_60] == 2
    )


def test_it_preserves_other_players_on_max_level_update(default_pupx):
    editor = RichPupxEditor()
    updated = editor.set_player_max_level(
        PlayerId.PLAYER_1, UpgradeId.TERRAN_INFANTRY_ARMOR, 0, default_pupx
    )
    for player in _GAME_PLAYERS:
        if player == PlayerId.PLAYER_1:
            continue
        assert all(v == 3 for v in updated.player_max_levels[player].values())
