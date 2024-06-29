""""""


import pytest

from richchk.editor.richchk.rich_uprp_editor import RichUprpEditor
from richchk.model.chk.uprp.uprp_constants import MAX_CUWP_SLOTS
from richchk.model.richchk.uprp.rich_uprp_section import RichUprpSection
from richchk.util.dataclasses_util import build_dataclass_with_fields

from ...fixtures.cuwp_fixtures import generate_cuwp_slot


@pytest.fixture(scope="function")
def rich_uprp():
    return RichUprpSection(_cuwp_slots=[generate_cuwp_slot(index=1)])


def test_integration_it_adds_cuwp_slots_and_allocates_ids_to_each(rich_uprp):
    editor = RichUprpEditor()
    cuwps_without_index = [
        build_dataclass_with_fields(
            generate_cuwp_slot(), _cloaked=False, _burrowed=True
        ),
        build_dataclass_with_fields(
            generate_cuwp_slot(), _cloaked=True, _burrowed=True
        ),
    ]
    expected_cuwps = rich_uprp.cuwp_slots + [
        build_dataclass_with_fields(cuwps_without_index[0], _index=2),
        build_dataclass_with_fields(cuwps_without_index[1], _index=3),
    ]
    new_uprp = editor.add_cuwp_slots(cuwps_without_index, rich_uprp)
    assert len(new_uprp.cuwp_slots) == 3
    for expected in expected_cuwps:
        assert expected in new_uprp.cuwp_slots


def test_integration_it_does_not_add_duplicate_cuwp_slots(rich_uprp):
    editor = RichUprpEditor()
    cuwp_to_add_without_index_duplicated = build_dataclass_with_fields(
        generate_cuwp_slot(), _cloaked=True, _burrowed=True
    )
    cuwp_to_add_with_index_duplicated = build_dataclass_with_fields(
        generate_cuwp_slot(), _cloaked=False, _burrowed=True, _invincible=True
    )
    cuwps_to_add = [
        cuwp_to_add_without_index_duplicated,
        cuwp_to_add_without_index_duplicated,
        cuwp_to_add_with_index_duplicated,
        cuwp_to_add_with_index_duplicated,
    ]
    expected_cuwps = rich_uprp.cuwp_slots + [
        build_dataclass_with_fields(cuwp_to_add_without_index_duplicated, _index=2),
        build_dataclass_with_fields(cuwp_to_add_with_index_duplicated, _index=100),
    ]
    new_uprp = editor.add_cuwp_slots(cuwps_to_add, rich_uprp)
    assert len(new_uprp.cuwp_slots) == 3
    for expected in expected_cuwps:
        assert expected in new_uprp.cuwp_slots


def test_integration_it_does_not_replace_cuwp_slots_already_in_uprp():
    editor = RichUprpEditor()
    cuwp_already_in_uprp = generate_cuwp_slot(index=1)
    uprp = RichUprpSection(_cuwp_slots=[generate_cuwp_slot(index=1)])
    cuwps_to_add = [cuwp_already_in_uprp]
    new_uprp = editor.add_cuwp_slots(cuwps_to_add, uprp)
    assert len(new_uprp.cuwp_slots) == len(uprp.cuwp_slots)
    assert cuwp_already_in_uprp in uprp.cuwp_slots
    assert cuwp_already_in_uprp in new_uprp.cuwp_slots


def test_integration_it_allocates_all_possible_ids(rich_uprp):
    editor = RichUprpEditor()
    cuwps_to_add = [
        build_dataclass_with_fields(generate_cuwp_slot(), _hitpoints_percentage=x)
        for x in range(2, MAX_CUWP_SLOTS + 1)
    ]
    new_uprp = editor.add_cuwp_slots(cuwps_to_add, rich_uprp)
    assert len(new_uprp.cuwp_slots) == MAX_CUWP_SLOTS


def test_integration_it_does_not_allocate_more_than_max_ids(rich_uprp):
    editor = RichUprpEditor()
    cuwps_to_add = [
        build_dataclass_with_fields(generate_cuwp_slot(), _hitpoints_percentage=x)
        for x in range(2, MAX_CUWP_SLOTS + 100)
    ]
    new_uprp = editor.add_cuwp_slots(cuwps_to_add, rich_uprp)
    assert len(new_uprp.cuwp_slots) == MAX_CUWP_SLOTS
