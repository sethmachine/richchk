from test.fixtures.location_fixtures import generate_rich_location_with_name

import pytest

from richchk.io.richchk.search.mrgn_search_util import MrgnSearchUtil
from richchk.model.richchk.mrgn.rich_mrgn_section import RichMrgnSection


def test_it_finds_location_by_exact_match():
    mrgn = RichMrgnSection(
        _locations=[
            generate_rich_location_with_name("loc1"),
            generate_rich_location_with_name("loc2"),
        ]
    )
    loc1 = MrgnSearchUtil.find_location_by_name("loc1", mrgn, ignorecase=False)
    assert loc1 == mrgn.locations[0]
    loc2 = MrgnSearchUtil.find_location_by_name("loc2", mrgn, ignorecase=False)
    assert loc2 == mrgn.locations[1]


def test_it_finds_location_by_exact_match_ignoring_case():
    mrgn = RichMrgnSection(
        _locations=[
            generate_rich_location_with_name("loc1"),
            generate_rich_location_with_name("loc2"),
        ]
    )
    loc1 = MrgnSearchUtil.find_location_by_name("LoC1", mrgn, ignorecase=True)
    assert loc1 == mrgn.locations[0]
    loc2 = MrgnSearchUtil.find_location_by_name("LOC2", mrgn, ignorecase=True)
    assert loc2 == mrgn.locations[1]


def test_it_finds_no_locations_exact_match_if_case_matters():
    mrgn = RichMrgnSection(
        _locations=[
            generate_rich_location_with_name("loc1"),
            generate_rich_location_with_name("loc2"),
        ]
    )
    assert not MrgnSearchUtil.find_location_by_name("LoC1", mrgn, ignorecase=False)
    assert not MrgnSearchUtil.find_location_by_name("LOC2", mrgn, ignorecase=False)


def test_it_finds_no_locations_exact_match_if_none_match():
    mrgn = RichMrgnSection(
        _locations=[
            generate_rich_location_with_name("loc1"),
            generate_rich_location_with_name("loc2"),
        ]
    )
    assert not MrgnSearchUtil.find_location_by_name("loc3", mrgn, ignorecase=False)


def test_it_finds_location_by_fuzzy_match():
    mrgn = RichMrgnSection(
        _locations=[
            generate_rich_location_with_name("my location"),
            generate_rich_location_with_name("my home"),
        ]
    )
    loc1 = MrgnSearchUtil.find_location_by_fuzzy_search("home", mrgn, ignorecase=False)
    assert loc1 == mrgn.locations[1]
    loc2 = MrgnSearchUtil.find_location_by_fuzzy_search(
        "location", mrgn, ignorecase=False
    )
    assert loc2 == mrgn.locations[0]


def test_it_throws_if_fuzzy_match_best_score_is_too_low():
    mrgn = RichMrgnSection(
        _locations=[
            generate_rich_location_with_name("my location"),
            generate_rich_location_with_name("my home"),
        ]
    )
    with pytest.raises(ValueError):
        MrgnSearchUtil.find_location_by_fuzzy_search(
            "home", mrgn, ignorecase=False, min_similarity=1.0
        )


def test_it_finds_location_by_fuzzy_match_ignoring_case():
    mrgn = RichMrgnSection(
        _locations=[
            generate_rich_location_with_name("my location"),
            generate_rich_location_with_name("my home"),
        ]
    )
    loc1 = MrgnSearchUtil.find_location_by_fuzzy_search("HoME", mrgn, ignorecase=True)
    assert loc1 == mrgn.locations[1]
    loc2 = MrgnSearchUtil.find_location_by_fuzzy_search(
        "LoCaTiOn", mrgn, ignorecase=True
    )
    assert loc2 == mrgn.locations[0]


def test_it_finds_location_by_fuzzy_match_preferring_case_agreement():
    mrgn = RichMrgnSection(
        _locations=[
            generate_rich_location_with_name("my LOCATION"),
            generate_rich_location_with_name("my location"),
        ]
    )
    loc1 = MrgnSearchUtil.find_location_by_fuzzy_search(
        "LOCATIon", mrgn, ignorecase=False
    )
    assert loc1 == mrgn.locations[0]
    loc2 = MrgnSearchUtil.find_location_by_fuzzy_search(
        "locatiON", mrgn, ignorecase=False
    )
    assert loc2 == mrgn.locations[1]
