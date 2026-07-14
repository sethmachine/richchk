import pytest

from richchk.editor.richchk.rich_pupx_editor import RichPupxEditor
from richchk.model.richchk.pupx.rich_pupx_section import RichPupxSection
from richchk.model.richchk.trig.player_id import PlayerId
from richchk.model.richchk.upgrades.upgrade_id import UpgradeId

_NUM_PLAYERS = 12
_NUM_UPGRADES = 61


def _make_pupx(
    player_max: int = 3,
    player_start: int = 0,
    global_max: int = 3,
    global_start: int = 0,
    player_defaults: bool = True,
) -> RichPupxSection:
    return RichPupxSection(
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
def default_pupx() -> RichPupxSection:
    return _make_pupx()


def test_it_sets_player_max_level(default_pupx):
    editor = RichPupxEditor()
    updated = editor.set_player_max_level(
        PlayerId.PLAYER_1, UpgradeId.TERRAN_INFANTRY_ARMOR, 2, default_pupx
    )
    assert updated.player_max_levels[0][0] == 2
    assert updated.player_max_levels[0][1] == 3


def test_it_does_not_mutate_original_on_max_level(default_pupx):
    editor = RichPupxEditor()
    editor.set_player_max_level(
        PlayerId.PLAYER_1, UpgradeId.TERRAN_INFANTRY_ARMOR, 2, default_pupx
    )
    assert default_pupx.player_max_levels[0][0] == 3


def test_it_sets_player_start_level(default_pupx):
    editor = RichPupxEditor()
    updated = editor.set_player_start_level(
        PlayerId.PLAYER_2, UpgradeId.TERRAN_VEHICLE_PLATING, 1, default_pupx
    )
    assert updated.player_start_levels[1][1] == 1
    assert updated.player_start_levels[0][0] == 0


def test_it_sets_player_uses_default(default_pupx):
    editor = RichPupxEditor()
    updated = editor.set_player_uses_default(
        PlayerId.PLAYER_1, UpgradeId.TERRAN_INFANTRY_ARMOR, False, default_pupx
    )
    assert updated.player_uses_defaults[0][0] is False
    assert updated.player_uses_defaults[0][1] is True


def test_it_raises_on_invalid_player(default_pupx):
    editor = RichPupxEditor()
    with pytest.raises(ValueError):
        editor.set_player_max_level(
            PlayerId.NONE, UpgradeId.TERRAN_INFANTRY_ARMOR, 1, default_pupx
        )


def test_it_allows_upgrade_id_60_bw_only(default_pupx):
    editor = RichPupxEditor()
    updated = editor.set_player_max_level(
        PlayerId.PLAYER_1, UpgradeId.UNKNOWN_UPGRADE_60, 2, default_pupx
    )
    assert updated.player_max_levels[0][60] == 2


def test_it_preserves_other_players_on_max_level_update(default_pupx):
    editor = RichPupxEditor()
    updated = editor.set_player_max_level(
        PlayerId.PLAYER_1, UpgradeId.TERRAN_INFANTRY_ARMOR, 0, default_pupx
    )
    for p in range(1, _NUM_PLAYERS):
        assert all(v == 3 for v in updated.player_max_levels[p])
