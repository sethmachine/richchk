import pytest

from richchk.editor.richchk.rich_upgr_editor import RichUpgrEditor
from richchk.model.richchk.trig.player_id import PlayerId
from richchk.model.richchk.upgr.rich_upgr_section import RichUpgrSection
from richchk.model.richchk.upgrades.upgrade_id import UpgradeId

_NUM_PLAYERS = 12
_NUM_UPGRADES = 46


def _make_upgr(
    player_max: int = 3,
    player_start: int = 0,
    global_max: int = 3,
    global_start: int = 0,
    player_defaults: bool = True,
) -> RichUpgrSection:
    return RichUpgrSection(
        _player_max_levels=[[player_max] * _NUM_UPGRADES for _ in range(_NUM_PLAYERS)],
        _player_start_levels=[
            [player_start] * _NUM_UPGRADES for _ in range(_NUM_PLAYERS)
        ],
        _global_max_levels=[global_max] * _NUM_UPGRADES,
        _global_start_levels=[global_start] * _NUM_UPGRADES,
        _player_uses_defaults=[
            [player_defaults] * _NUM_UPGRADES for _ in range(_NUM_PLAYERS)
        ],
    )


@pytest.fixture
def default_upgr() -> RichUpgrSection:
    return _make_upgr()


def test_it_sets_player_max_level(default_upgr):
    editor = RichUpgrEditor()
    updated = editor.set_player_max_level(
        PlayerId.PLAYER_1, UpgradeId.TERRAN_INFANTRY_ARMOR, 2, default_upgr
    )
    assert updated.player_max_levels[0][0] == 2
    assert updated.player_max_levels[0][1] == 3


def test_it_does_not_mutate_original_on_max_level(default_upgr):
    editor = RichUpgrEditor()
    editor.set_player_max_level(
        PlayerId.PLAYER_1, UpgradeId.TERRAN_INFANTRY_ARMOR, 2, default_upgr
    )
    assert default_upgr.player_max_levels[0][0] == 3


def test_it_sets_player_start_level(default_upgr):
    editor = RichUpgrEditor()
    updated = editor.set_player_start_level(
        PlayerId.PLAYER_2, UpgradeId.TERRAN_VEHICLE_PLATING, 1, default_upgr
    )
    assert updated.player_start_levels[1][1] == 1
    assert updated.player_start_levels[0][0] == 0


def test_it_sets_player_uses_default(default_upgr):
    editor = RichUpgrEditor()
    updated = editor.set_player_uses_default(
        PlayerId.PLAYER_1, UpgradeId.TERRAN_INFANTRY_ARMOR, False, default_upgr
    )
    assert updated.player_uses_defaults[0][0] is False
    assert updated.player_uses_defaults[0][1] is True


def test_it_raises_on_invalid_player(default_upgr):
    editor = RichUpgrEditor()
    with pytest.raises(ValueError):
        editor.set_player_max_level(
            PlayerId.NONE, UpgradeId.TERRAN_INFANTRY_ARMOR, 1, default_upgr
        )


def test_it_raises_on_upgrade_id_out_of_range(default_upgr):
    editor = RichUpgrEditor()
    with pytest.raises(ValueError):
        editor.set_player_max_level(
            PlayerId.PLAYER_1, UpgradeId.UNKNOWN_UPGRADE_60, 1, default_upgr
        )


def test_it_preserves_other_players_on_max_level_update(default_upgr):
    editor = RichUpgrEditor()
    updated = editor.set_player_max_level(
        PlayerId.PLAYER_1, UpgradeId.TERRAN_INFANTRY_ARMOR, 0, default_upgr
    )
    for p in range(1, _NUM_PLAYERS):
        assert all(v == 3 for v in updated.player_max_levels[p])
