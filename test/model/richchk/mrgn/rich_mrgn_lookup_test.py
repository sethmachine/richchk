import pytest

from richchk.model.richchk.mrgn.rich_location import RichLocation, RichNullLocation
from richchk.model.richchk.mrgn.rich_mrgn_lookup import RichMrgnLookup
from richchk.model.richchk.str.rich_string import RichNullString, RichString


@pytest.fixture(scope="function")
def used_location():
    return RichLocation(
        10, 20, 30, 40, RichString(_value="used"), _index=3, _low_air=False
    )


@pytest.fixture(scope="function")
def lookup(used_location):
    return RichMrgnLookup(
        _location_by_id_lookup={3: used_location},
        _id_by_location_lookup={used_location: 3},
    )


def test_it_finds_a_used_location_by_id(lookup, used_location):
    assert lookup.get_location_by_id(3) == used_location
    assert lookup.get_id_by_location(used_location) == 3


def test_it_still_reports_unallocated_ids_as_missing_when_checking_existence(lookup):
    assert lookup.get_location_by_id(0) is None
    assert lookup.get_location_by_id(14) is None
    with pytest.raises(ValueError):
        lookup.get_location_by_id_or_throw(14)


def test_it_resolves_no_location_id_to_a_null_location(lookup):
    location = lookup.resolve_location_id(0)
    assert isinstance(location, RichNullLocation)
    assert lookup.resolve_location_id_or_throw(0) == RichNullLocation()


def test_it_encodes_a_null_location_as_id_zero_even_if_it_is_not_in_the_lookup(
    lookup,
):
    assert lookup.get_id_by_location(RichNullLocation()) == 0
    assert lookup.get_id_by_location_or_throw(RichNullLocation()) == 0


def test_it_builds_equal_null_locations():
    assert RichNullLocation() == RichNullLocation()
    assert hash(RichNullLocation()) == hash(RichNullLocation())


def test_it_resolves_an_empty_slot_id_to_an_unused_slot_with_that_index(lookup):
    location = lookup.resolve_location_id(14)
    assert not isinstance(location, RichNullLocation)
    assert location.index == 14
    assert location.is_unused_slot
    assert lookup.get_id_by_location_or_throw(location) == 14
    assert lookup.resolve_location_id_or_throw(14) == location


def test_it_returns_none_for_ids_beyond_the_last_slot(lookup):
    assert lookup.resolve_location_id(256) is None
    with pytest.raises(ValueError):
        lookup.resolve_location_id_or_throw(256)


def test_it_does_not_give_an_id_to_an_unindexed_blank_location(lookup):
    blank_without_index = RichLocation(0, 0, 0, 0, RichNullString())
    assert lookup.get_id_by_location(blank_without_index) is None
    with pytest.raises(ValueError):
        lookup.get_id_by_location_or_throw(blank_without_index)


def test_it_does_not_treat_a_named_or_sized_location_as_an_unused_slot(lookup):
    named = RichLocation(0, 0, 0, 0, RichString(_value="named"), _index=9)
    sized = RichLocation(0, 0, 1, 0, RichNullString(), _index=9)
    assert not named.is_unused_slot
    assert not sized.is_unused_slot
    assert lookup.get_id_by_location(named) is None
    assert lookup.get_id_by_location(sized) is None
