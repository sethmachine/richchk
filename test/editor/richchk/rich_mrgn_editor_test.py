""""""


import pytest

from richchk.editor.richchk.rich_mrgn_editor import RichMrgnEditor
from richchk.model.chk.mrgn.mrgn_constants import ANYWHERE_LOCATION_ID, MAX_LOCATIONS
from richchk.model.richchk.mrgn.rich_mrgn_section import RichMrgnSection
from richchk.util.dataclasses_util import build_dataclass_with_fields

from ...fixtures.location_fixtures import generate_rich_location


@pytest.fixture(scope="function")
def rich_mrgn():
    return RichMrgnSection(_locations=[generate_rich_location(index=1)])


def test_integration_it_adds_locations_to_mrgn_and_allocates_index_to_each(rich_mrgn):
    editor = RichMrgnEditor()
    locations_to_add_without_index = [
        generate_rich_location(),
        generate_rich_location(),
    ]
    expected_locations = rich_mrgn.locations + [
        build_dataclass_with_fields(locations_to_add_without_index[0], _index=2),
        build_dataclass_with_fields(locations_to_add_without_index[1], _index=3),
    ]
    new_mrgn, _ = editor.add_locations(locations_to_add_without_index, rich_mrgn)
    assert len(new_mrgn.locations) == 3
    for expected in expected_locations:
        assert expected in new_mrgn.locations


def test_integration_it_does_not_add_duplicate_locations(rich_mrgn):
    editor = RichMrgnEditor()
    loc1_to_add = generate_rich_location()
    loc2_to_add_with_index = generate_rich_location(index=100)
    locations_to_add = [
        loc1_to_add,
        loc1_to_add,
        loc2_to_add_with_index,
        loc2_to_add_with_index,
    ]
    expected_locations = rich_mrgn.locations + [
        build_dataclass_with_fields(loc1_to_add, _index=2),
        build_dataclass_with_fields(loc2_to_add_with_index, _index=100),
    ]
    new_mrgn, _ = editor.add_locations(locations_to_add, rich_mrgn)
    assert len(new_mrgn.locations) == 3
    for expected in expected_locations:
        assert expected in new_mrgn.locations


def test_integration_it_does_not_replace_locations_already_in_mrgn():
    editor = RichMrgnEditor()
    dup_loc_to_add_with_index = generate_rich_location(index=100)
    mrgn = RichMrgnSection(
        _locations=[
            generate_rich_location(index=1),
            dup_loc_to_add_with_index,
        ]
    )
    locations_to_add = [dup_loc_to_add_with_index]
    new_mrgn, _ = editor.add_locations(locations_to_add, mrgn)
    assert len(new_mrgn.locations) == len(mrgn.locations)


def test_integration_it_does_not_allocate_anywhere_location_id(rich_mrgn):
    editor = RichMrgnEditor()
    locations_to_add_without_index = [
        generate_rich_location() for x in range(1, ANYWHERE_LOCATION_ID + 2)
    ]
    new_mrgn, _ = editor.add_locations(locations_to_add_without_index, rich_mrgn)
    assert len(new_mrgn.locations) == (ANYWHERE_LOCATION_ID + 1) + len(
        rich_mrgn.locations
    )
    for loc in new_mrgn.locations:
        assert loc.index != ANYWHERE_LOCATION_ID


def test_integration_it_allocates_all_possible_location_ids(rich_mrgn):
    editor = RichMrgnEditor()
    # 2 locations are already allocated: 1 in rich mrgn and 1 for ANYWHERE
    locations_to_add_without_index = [
        generate_rich_location() for x in range(1, MAX_LOCATIONS - 1)
    ]
    new_mrgn, _ = editor.add_locations(locations_to_add_without_index, rich_mrgn)
    # ANYWHERE is not included in this example
    assert len(new_mrgn.locations) == MAX_LOCATIONS - 1


def test_integration_it_does_not_allocate_more_locations_than_max(rich_mrgn):
    editor = RichMrgnEditor()
    locations_to_add_without_index = [
        generate_rich_location() for x in range(1, MAX_LOCATIONS + 100)
    ]
    new_mrgn, _ = editor.add_locations(locations_to_add_without_index, rich_mrgn)
    # ANYWHERE is not included in this example
    assert len(new_mrgn.locations) == MAX_LOCATIONS - 1
