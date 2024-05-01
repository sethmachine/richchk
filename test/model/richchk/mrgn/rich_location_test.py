"""Verify equality works as expected given we have custom overrides for __eq__ and
__hash__"""

from chkjson.model.richchk.mrgn.rich_location import RichLocation
from chkjson.model.richchk.str.rich_string import RichString


def test_locations_are_not_equal_if_all_fields_match_but_no_index_defined():
    loc1 = RichLocation(0, 0, 0, 0, RichString(_value="location 1"), _index=None)
    loc2 = RichLocation(0, 0, 0, 0, RichString(_value="location 1"), _index=None)
    assert loc1 != loc2


def test_locations_are_unique_in_set_if_all_fields_match_but_no_index_defined():
    loc1 = RichLocation(0, 0, 0, 0, RichString(_value="location 1"), _index=None)
    loc2 = RichLocation(0, 0, 0, 0, RichString(_value="location 1"), _index=None)
    loc_set = {loc1, loc2}
    assert loc1 in loc_set
    assert loc2 in loc_set
    assert len(loc_set) == 2


def test_locations_are_the_same_if_index_defined_and_all_fields_match():
    loc1 = RichLocation(0, 0, 0, 0, RichString(_value="location 1"), _index=1)
    loc2 = RichLocation(0, 0, 0, 0, RichString(_value="location 1"), _index=1)
    assert loc1 == loc2


def test_locations_are_not_unique_in_set_if_index_defined_and_all_fields_match():
    loc1 = RichLocation(0, 0, 0, 0, RichString(_value="location 1"), _index=1)
    loc2 = RichLocation(0, 0, 0, 0, RichString(_value="location 1"), _index=1)
    loc_set = {loc1, loc2}
    assert loc1 in loc_set
    assert loc2 in loc_set
    assert len(loc_set) == 1


def test_locations_not_equal_or_unique_if_atleast_one_has_undefined_index():
    loc1 = RichLocation(0, 0, 0, 0, RichString(_value="location 1"), _index=1)
    loc2 = RichLocation(0, 0, 0, 0, RichString(_value="location 1"), _index=None)
    loc_set = {loc1, loc2}
    assert loc1 != loc2
    assert loc1 in loc_set
    assert loc2 in loc_set
    assert len(loc_set) == 2


def test_locations_not_equal_if_values_different_with_defined_index():
    loc1 = RichLocation(0, 0, 0, 0, RichString(_value="location 1"), _index=1)
    loc2 = RichLocation(0, 0, 0, 0, RichString(_value="location 1"), _index=2)
    assert loc1 != loc2
