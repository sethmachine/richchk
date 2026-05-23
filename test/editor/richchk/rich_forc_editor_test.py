import pytest

from richchk.editor.richchk.rich_forc_editor import RichForcEditor
from richchk.model.richchk.forc.force_flags import ForceFlags
from richchk.model.richchk.forc.force_id import ForceId
from richchk.model.richchk.forc.rich_forc_section import RichForcSection
from richchk.model.richchk.forc.rich_force import RichForce
from richchk.model.richchk.str.rich_string import RichString
from richchk.model.richchk.trig.player_id import PlayerId

_NUM_PLAYERS = 8
_NUM_FORCES = 4

_DEFAULT_FLAGS = ForceFlags()
_DEFAULT_FORCES = [RichForce() for _ in range(_NUM_FORCES)]
_DEFAULT_ASSIGNMENTS = [ForceId.FORCE_1] * _NUM_PLAYERS


@pytest.fixture
def empty_forc() -> RichForcSection:
    return RichForcSection(
        _player_force_assignments=list(_DEFAULT_ASSIGNMENTS),
        _forces=list(_DEFAULT_FORCES),
    )


def test_it_adds_player_to_force(empty_forc):
    editor = RichForcEditor()
    updated = editor.add_player_to_force(PlayerId.PLAYER_3, ForceId.FORCE_2, empty_forc)
    assert updated.player_force_assignments[2] == ForceId.FORCE_2
    assert updated.player_force_assignments[0] == ForceId.FORCE_1
    assert updated.player_force_assignments[1] == ForceId.FORCE_1


def test_it_does_not_mutate_original_on_assignment(empty_forc):
    editor = RichForcEditor()
    editor.add_player_to_force(PlayerId.PLAYER_1, ForceId.FORCE_3, empty_forc)
    assert empty_forc.player_force_assignments[0] == ForceId.FORCE_1


def test_it_updates_force(empty_forc):
    editor = RichForcEditor()
    new_force = RichForce(
        _name=RichString(_value="Alliance"),
        _flags=ForceFlags(_allies=True, _allied_victory=True),
    )
    updated = editor.update_force(ForceId.FORCE_1, new_force, empty_forc)
    assert updated.forces[0] == new_force
    assert updated.forces[1:] == list(_DEFAULT_FORCES)[1:]


def test_it_sets_force_flags_via_rich_force(empty_forc):
    editor = RichForcEditor()
    new_flags = ForceFlags(_allies=True, _shared_vision=True)
    updated = editor.update_force(ForceId.FORCE_2, RichForce(_flags=new_flags), empty_forc)
    assert updated.forces[1].flags == new_flags
    assert updated.forces[0].flags == _DEFAULT_FLAGS


def test_it_preserves_force_name_when_updating_flags(empty_forc):
    editor = RichForcEditor()
    named_force = RichForce(_name=RichString(_value="Team Alpha"))
    forc_with_name = editor.update_force(ForceId.FORCE_1, named_force, empty_forc)
    updated = editor.update_force(
        ForceId.FORCE_1,
        RichForce(_name=forc_with_name.forces[0].name, _flags=ForceFlags(_allied_victory=True)),
        forc_with_name,
    )
    assert updated.forces[0].name == RichString(_value="Team Alpha")
    assert updated.forces[0].flags.allied_victory is True


def test_it_raises_on_invalid_player_slot(empty_forc):
    editor = RichForcEditor()
    with pytest.raises(ValueError):
        editor.add_player_to_force(PlayerId.PLAYER_9, ForceId.FORCE_1, empty_forc)
