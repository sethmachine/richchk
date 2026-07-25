import pytest

from richchk.editor.richchk.rich_ptex_editor import RichPtexEditor
from richchk.model.richchk.ptex.rich_ptex_section import RichPtexSection
from richchk.model.richchk.techs.tech_id import TechId
from richchk.model.richchk.trig.player_id import PlayerId

_GAME_PLAYERS = [p for p in PlayerId if p.id < 12]
_ALL_TECHS = list(TechId)


def _make_ptex(
    player_avail: bool = True,
    player_researched: bool = False,
    global_avail: bool = True,
    global_researched: bool = False,
    player_defaults: bool = True,
) -> RichPtexSection:
    return RichPtexSection(
        _player_tech_availability={
            p: {t: player_avail for t in _ALL_TECHS} for p in _GAME_PLAYERS
        },
        _player_tech_researched={
            p: {t: player_researched for t in _ALL_TECHS} for p in _GAME_PLAYERS
        },
        _global_tech_availability={t: global_avail for t in _ALL_TECHS},
        _global_tech_researched={t: global_researched for t in _ALL_TECHS},
        _player_uses_defaults={
            p: {t: player_defaults for t in _ALL_TECHS} for p in _GAME_PLAYERS
        },
    )


@pytest.fixture
def default_ptex() -> RichPtexSection:
    return _make_ptex()


def test_it_sets_tech_available_for_player(default_ptex):
    editor = RichPtexEditor()
    updated = editor.set_tech_available_for_player(
        PlayerId.PLAYER_1, TechId.STIM_PACKS, False, default_ptex
    )
    assert (
        updated.player_tech_availability[PlayerId.PLAYER_1][TechId.STIM_PACKS] is False
    )
    assert updated.player_tech_availability[PlayerId.PLAYER_1][TechId.LOCKDOWN] is True


def test_it_sets_bw_tech_available_for_player(default_ptex):
    editor = RichPtexEditor()
    updated = editor.set_tech_available_for_player(
        PlayerId.PLAYER_1, TechId.RESTORATION, False, default_ptex
    )
    assert (
        updated.player_tech_availability[PlayerId.PLAYER_1][TechId.RESTORATION] is False
    )
    assert (
        updated.player_tech_availability[PlayerId.PLAYER_1][TechId.STIM_PACKS] is True
    )


def test_it_does_not_mutate_original_on_tech_availability(default_ptex):
    editor = RichPtexEditor()
    editor.set_tech_available_for_player(
        PlayerId.PLAYER_1, TechId.STIM_PACKS, False, default_ptex
    )
    assert (
        default_ptex.player_tech_availability[PlayerId.PLAYER_1][TechId.STIM_PACKS]
        is True
    )


def test_it_sets_tech_researched_for_player(default_ptex):
    editor = RichPtexEditor()
    updated = editor.set_tech_researched_for_player(
        PlayerId.PLAYER_2, TechId.LOCKDOWN, True, default_ptex
    )
    assert updated.player_tech_researched[PlayerId.PLAYER_2][TechId.LOCKDOWN] is True
    assert updated.player_tech_researched[PlayerId.PLAYER_1][TechId.STIM_PACKS] is False


def test_it_sets_player_uses_default(default_ptex):
    editor = RichPtexEditor()
    updated = editor.set_player_uses_default(
        PlayerId.PLAYER_1, TechId.STIM_PACKS, False, default_ptex
    )
    assert updated.player_uses_defaults[PlayerId.PLAYER_1][TechId.STIM_PACKS] is False
    assert updated.player_uses_defaults[PlayerId.PLAYER_1][TechId.LOCKDOWN] is True


def test_it_sets_uses_defaults_false_on_tech_availability_override(default_ptex):
    editor = RichPtexEditor()
    updated = editor.set_tech_available_for_player(
        PlayerId.PLAYER_1, TechId.STIM_PACKS, False, default_ptex
    )
    assert updated.player_uses_defaults[PlayerId.PLAYER_1][TechId.STIM_PACKS] is False
    assert updated.player_uses_defaults[PlayerId.PLAYER_1][TechId.LOCKDOWN] is True


def test_it_sets_uses_defaults_false_on_tech_researched_override(default_ptex):
    editor = RichPtexEditor()
    updated = editor.set_tech_researched_for_player(
        PlayerId.PLAYER_1, TechId.STIM_PACKS, True, default_ptex
    )
    assert updated.player_uses_defaults[PlayerId.PLAYER_1][TechId.STIM_PACKS] is False
    assert updated.player_uses_defaults[PlayerId.PLAYER_1][TechId.LOCKDOWN] is True


def test_it_preserves_other_players_on_tech_availability_update(default_ptex):
    editor = RichPtexEditor()
    updated = editor.set_tech_available_for_player(
        PlayerId.PLAYER_1, TechId.STIM_PACKS, False, default_ptex
    )
    for player in _GAME_PLAYERS:
        if player == PlayerId.PLAYER_1:
            continue
        assert all(updated.player_tech_availability[player].values())


def test_apply_player_tech_availability_merges_partial_dict(default_ptex):
    editor = RichPtexEditor()
    updates = {
        PlayerId.PLAYER_1: {TechId.STIM_PACKS: False, TechId.RESTORATION: False},
        PlayerId.PLAYER_2: {TechId.RESTORATION: False},
    }
    updated = editor.apply_player_tech_availability(updates, default_ptex)
    assert (
        updated.player_tech_availability[PlayerId.PLAYER_1][TechId.STIM_PACKS] is False
    )
    assert (
        updated.player_tech_availability[PlayerId.PLAYER_1][TechId.RESTORATION] is False
    )
    assert (
        updated.player_tech_availability[PlayerId.PLAYER_2][TechId.RESTORATION] is False
    )
    assert (
        updated.player_tech_availability[PlayerId.PLAYER_1][TechId.ARCHON_WARP] is True
    )
    assert (
        updated.player_tech_availability[PlayerId.PLAYER_3][TechId.STIM_PACKS] is True
    )
    assert updated.player_uses_defaults[PlayerId.PLAYER_1][TechId.STIM_PACKS] is False
    assert updated.player_uses_defaults[PlayerId.PLAYER_1][TechId.ARCHON_WARP] is True


def test_apply_player_tech_researched_merges_partial_dict(default_ptex):
    editor = RichPtexEditor()
    updates = {
        PlayerId.PLAYER_1: {TechId.RESTORATION: True},
        PlayerId.PLAYER_2: {TechId.LOCKDOWN: True},
    }
    updated = editor.apply_player_tech_researched(updates, default_ptex)
    assert updated.player_tech_researched[PlayerId.PLAYER_1][TechId.RESTORATION] is True
    assert updated.player_tech_researched[PlayerId.PLAYER_2][TechId.LOCKDOWN] is True
    assert updated.player_tech_researched[PlayerId.PLAYER_1][TechId.LOCKDOWN] is False
    assert updated.player_uses_defaults[PlayerId.PLAYER_1][TechId.RESTORATION] is False
    assert updated.player_uses_defaults[PlayerId.PLAYER_1][TechId.LOCKDOWN] is True
