import pytest

from richchk.editor.richchk.rich_ptec_editor import RichPtecEditor
from richchk.model.richchk.ptec.rich_ptec_section import RichPtecSection
from richchk.model.richchk.techs.tech_id import TechId
from richchk.model.richchk.trig.player_id import PlayerId

_NUM_PLAYERS = 12
_NUM_TECHS = 24


def _make_ptec(
    player_avail: bool = True,
    player_researched: bool = False,
    global_avail: bool = True,
    global_researched: bool = False,
    player_defaults: bool = True,
) -> RichPtecSection:
    return RichPtecSection(
        _player_tech_availability=[
            [player_avail] * _NUM_TECHS for _ in range(_NUM_PLAYERS)
        ],
        _player_tech_researched=[
            [player_researched] * _NUM_TECHS for _ in range(_NUM_PLAYERS)
        ],
        _global_tech_availability=[global_avail] * _NUM_TECHS,
        _global_tech_researched=[global_researched] * _NUM_TECHS,
        _player_uses_defaults=[
            [player_defaults] * _NUM_TECHS for _ in range(_NUM_PLAYERS)
        ],
    )


@pytest.fixture
def default_ptec() -> RichPtecSection:
    return _make_ptec()


def test_it_sets_tech_available_for_player(default_ptec):
    editor = RichPtecEditor()
    updated = editor.set_tech_available_for_player(
        PlayerId.PLAYER_1, TechId.STIM_PACKS, False, default_ptec
    )
    assert updated.player_tech_availability[0][0] is False
    assert updated.player_tech_availability[0][1] is True


def test_it_does_not_mutate_original_on_tech_availability(default_ptec):
    editor = RichPtecEditor()
    editor.set_tech_available_for_player(
        PlayerId.PLAYER_1, TechId.STIM_PACKS, False, default_ptec
    )
    assert default_ptec.player_tech_availability[0][0] is True


def test_it_sets_tech_researched_for_player(default_ptec):
    editor = RichPtecEditor()
    updated = editor.set_tech_researched_for_player(
        PlayerId.PLAYER_2, TechId.LOCKDOWN, True, default_ptec
    )
    assert updated.player_tech_researched[1][1] is True
    assert updated.player_tech_researched[0][0] is False


def test_it_sets_player_uses_default(default_ptec):
    editor = RichPtecEditor()
    updated = editor.set_player_uses_default(
        PlayerId.PLAYER_1, TechId.STIM_PACKS, False, default_ptec
    )
    assert updated.player_uses_defaults[0][0] is False
    assert updated.player_uses_defaults[0][1] is True


def test_it_raises_on_invalid_player(default_ptec):
    editor = RichPtecEditor()
    with pytest.raises(ValueError):
        editor.set_tech_available_for_player(
            PlayerId.NONE, TechId.STIM_PACKS, False, default_ptec
        )


def test_it_preserves_other_players_on_tech_availability_update(default_ptec):
    editor = RichPtecEditor()
    updated = editor.set_tech_available_for_player(
        PlayerId.PLAYER_1, TechId.STIM_PACKS, False, default_ptec
    )
    for p in range(1, _NUM_PLAYERS):
        assert all(updated.player_tech_availability[p])
