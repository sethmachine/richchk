import pytest

from richchk.editor.richchk.rich_ptec_editor import RichPtecEditor
from richchk.model.richchk.ptec.rich_ptec_section import RichPtecSection
from richchk.model.richchk.techs.tech_id import TechId
from richchk.model.richchk.trig.player_id import PlayerId

_GAME_PLAYERS = [p for p in PlayerId if p.id < 12]
_TECHS = list(TechId)


def _make_ptec(
    player_avail: bool = True,
    player_researched: bool = False,
    global_avail: bool = True,
    global_researched: bool = False,
    player_defaults: bool = True,
) -> RichPtecSection:
    return RichPtecSection(
        _player_tech_availability={
            p: {t: player_avail for t in _TECHS} for p in _GAME_PLAYERS
        },
        _player_tech_researched={
            p: {t: player_researched for t in _TECHS} for p in _GAME_PLAYERS
        },
        _global_tech_availability={t: global_avail for t in _TECHS},
        _global_tech_researched={t: global_researched for t in _TECHS},
        _player_uses_defaults={
            p: {t: player_defaults for t in _TECHS} for p in _GAME_PLAYERS
        },
    )


@pytest.fixture
def default_ptec() -> RichPtecSection:
    return _make_ptec()


def test_it_sets_tech_available_for_player(default_ptec):
    editor = RichPtecEditor()
    updated = editor.set_tech_available_for_player(
        PlayerId.PLAYER_1, TechId.STIM_PACKS, False, default_ptec
    )
    assert (
        updated.player_tech_availability[PlayerId.PLAYER_1][TechId.STIM_PACKS] is False
    )
    assert updated.player_tech_availability[PlayerId.PLAYER_1][TechId.LOCKDOWN] is True


def test_it_does_not_mutate_original_on_tech_availability(default_ptec):
    editor = RichPtecEditor()
    editor.set_tech_available_for_player(
        PlayerId.PLAYER_1, TechId.STIM_PACKS, False, default_ptec
    )
    assert (
        default_ptec.player_tech_availability[PlayerId.PLAYER_1][TechId.STIM_PACKS]
        is True
    )


def test_it_sets_tech_researched_for_player(default_ptec):
    editor = RichPtecEditor()
    updated = editor.set_tech_researched_for_player(
        PlayerId.PLAYER_2, TechId.LOCKDOWN, True, default_ptec
    )
    assert updated.player_tech_researched[PlayerId.PLAYER_2][TechId.LOCKDOWN] is True
    assert updated.player_tech_researched[PlayerId.PLAYER_1][TechId.STIM_PACKS] is False


def test_it_sets_player_uses_default(default_ptec):
    editor = RichPtecEditor()
    updated = editor.set_player_uses_default(
        PlayerId.PLAYER_1, TechId.STIM_PACKS, False, default_ptec
    )
    assert updated.player_uses_defaults[PlayerId.PLAYER_1][TechId.STIM_PACKS] is False
    assert updated.player_uses_defaults[PlayerId.PLAYER_1][TechId.LOCKDOWN] is True


def test_it_sets_uses_defaults_false_on_tech_availability_override(default_ptec):
    editor = RichPtecEditor()
    updated = editor.set_tech_available_for_player(
        PlayerId.PLAYER_1, TechId.STIM_PACKS, False, default_ptec
    )
    assert updated.player_uses_defaults[PlayerId.PLAYER_1][TechId.STIM_PACKS] is False
    assert updated.player_uses_defaults[PlayerId.PLAYER_1][TechId.LOCKDOWN] is True


def test_it_sets_uses_defaults_false_on_tech_researched_override(default_ptec):
    editor = RichPtecEditor()
    updated = editor.set_tech_researched_for_player(
        PlayerId.PLAYER_1, TechId.STIM_PACKS, True, default_ptec
    )
    assert updated.player_uses_defaults[PlayerId.PLAYER_1][TechId.STIM_PACKS] is False
    assert updated.player_uses_defaults[PlayerId.PLAYER_1][TechId.LOCKDOWN] is True


def test_it_preserves_other_players_on_tech_availability_update(default_ptec):
    editor = RichPtecEditor()
    updated = editor.set_tech_available_for_player(
        PlayerId.PLAYER_1, TechId.STIM_PACKS, False, default_ptec
    )
    for player in _GAME_PLAYERS:
        if player == PlayerId.PLAYER_1:
            continue
        assert all(updated.player_tech_availability[player].values())


def test_apply_player_tech_availability_merges_partial_dict(default_ptec):
    editor = RichPtecEditor()
    updates = {
        PlayerId.PLAYER_1: {TechId.STIM_PACKS: False, TechId.LOCKDOWN: False},
        PlayerId.PLAYER_2: {TechId.STIM_PACKS: False},
    }
    updated = editor.apply_player_tech_availability(updates, default_ptec)
    assert (
        updated.player_tech_availability[PlayerId.PLAYER_1][TechId.STIM_PACKS] is False
    )
    assert updated.player_tech_availability[PlayerId.PLAYER_1][TechId.LOCKDOWN] is False
    assert (
        updated.player_tech_availability[PlayerId.PLAYER_2][TechId.STIM_PACKS] is False
    )
    assert (
        updated.player_tech_availability[PlayerId.PLAYER_1][TechId.ARCHON_WARP] is True
    )
    assert (
        updated.player_tech_availability[PlayerId.PLAYER_3][TechId.STIM_PACKS] is True
    )
    assert updated.player_uses_defaults[PlayerId.PLAYER_1][TechId.STIM_PACKS] is False
    assert updated.player_uses_defaults[PlayerId.PLAYER_1][TechId.ARCHON_WARP] is True


def test_apply_player_tech_researched_merges_partial_dict(default_ptec):
    editor = RichPtecEditor()
    updates = {
        PlayerId.PLAYER_1: {TechId.STIM_PACKS: True},
        PlayerId.PLAYER_2: {TechId.LOCKDOWN: True},
    }
    updated = editor.apply_player_tech_researched(updates, default_ptec)
    assert updated.player_tech_researched[PlayerId.PLAYER_1][TechId.STIM_PACKS] is True
    assert updated.player_tech_researched[PlayerId.PLAYER_2][TechId.LOCKDOWN] is True
    assert updated.player_tech_researched[PlayerId.PLAYER_1][TechId.LOCKDOWN] is False
    assert updated.player_uses_defaults[PlayerId.PLAYER_1][TechId.STIM_PACKS] is False
    assert updated.player_uses_defaults[PlayerId.PLAYER_1][TechId.LOCKDOWN] is True
