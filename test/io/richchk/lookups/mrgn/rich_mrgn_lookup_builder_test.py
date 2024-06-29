import pytest

from richchk.io.richchk.lookups.mrgn.rich_mrgn_lookup_builder import (
    RichMrgnLookupBuilder,
)
from richchk.model.richchk.mrgn.rich_location import RichLocation
from richchk.model.richchk.mrgn.rich_mrgn_section import RichMrgnSection
from richchk.model.richchk.str.rich_string import RichString


@pytest.fixture(scope="function")
def rich_mrgn():
    return RichMrgnSection(
        _locations=[
            RichLocation(1, 1, 1, 1, RichString(_value="location 1"), _index=1),
            RichLocation(2, 2, 2, 2, RichString(_value="location 2"), _index=2),
        ]
    )


def test_integration_it_builds_lookup_with_expected_structure(rich_mrgn):
    lookup = RichMrgnLookupBuilder().build_lookup(rich_mrgn=rich_mrgn)
    assert len(lookup._location_by_id_lookup) == len(rich_mrgn.locations)
    for rich_location in rich_mrgn.locations:
        maybe_rich_location = lookup.get_location_by_id(rich_location.index)
        assert rich_location == maybe_rich_location
        assert lookup.get_id_by_location(rich_location) == rich_location.index
