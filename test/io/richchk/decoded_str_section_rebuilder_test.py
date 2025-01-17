"""Test.

TODO: make a util to query RichChk/Chk objects ?

TODO: implement or add a dependency for a generic Builder pattern TODO: learn about how
to mock objects in pytest framework
"""
import pytest

from richchk.io.richchk.decoded_str_section_rebuilder import DecodedStrSectionRebuilder
from richchk.model.chk.str.decoded_str_section import DecodedStrSection
from richchk.model.richchk.rich_chk import RichChk
from richchk.model.richchk.str.rich_string import RichString
from richchk.model.richchk.unis.rich_unis_section import RichUnisSection
from richchk.model.richchk.unis.unit_id import UnitId
from richchk.model.richchk.unis.unit_setting import UnitSetting
from richchk.transcoder.chk.transcoders.chk_str_transcoder import ChkStrTranscoder

from ...chk_resources import CHK_SECTION_FILE_PATHS

_RICH_UNIS_NEWLY_ADDED_STRING = "a newly added string"
_EXPECTED_STRINGS_IN_DECODED_STR = [
    "test-string-1-marine",
    "test-string-2-firebat",
    "test-string-3-ghost",
]


@pytest.fixture(scope="function")
def decoded_str_section() -> DecodedStrSection:
    # these strings were added into the CHK section by using a GUI map editor
    # _EXPECTED_STRINGS_WITH_ID = [
    #     {"string": "test-string-1-marine", "id": 8},
    #     {"string": "test-string-2-firebat", "id": 9},
    #     {"string": "test-string-3-ghost", "id": 10},
    # ]
    with open(
        CHK_SECTION_FILE_PATHS[DecodedStrSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return ChkStrTranscoder().decode(chk_binary_data)


@pytest.fixture(scope="function")
def rich_unis_with_new_string():
    return RichUnisSection(
        _unit_settings=[
            UnitSetting(
                _unit_id=UnitId.TERRAN_MARINE,
                _hitpoints=100,
                _shieldpoints=100,
                _armorpoints=100,
                _build_time=100,
                _mineral_cost=100,
                _gas_cost=100,
                _custom_unit_name=RichString(_value=_RICH_UNIS_NEWLY_ADDED_STRING),
                _weapons=[],
            )
        ]
    )


@pytest.fixture(scope="function")
def rich_unis_with_already_existing_string():
    return RichUnisSection(
        _unit_settings=[
            UnitSetting(
                _unit_id=UnitId.TERRAN_MARINE,
                _hitpoints=100,
                _shieldpoints=100,
                _armorpoints=100,
                _build_time=100,
                _mineral_cost=100,
                _gas_cost=100,
                _custom_unit_name=RichString(
                    _value=_EXPECTED_STRINGS_IN_DECODED_STR[0]
                ),
                _weapons=[],
            )
        ]
    )


@pytest.fixture(scope="function")
def rich_chk_with_new_rich_strings():
    empty_decoded_str = DecodedStrSection(
        _number_of_strings=0, _string_offsets=[], _strings=[]
    )
    rich_unis = RichUnisSection(
        _unit_settings=[
            UnitSetting(
                _unit_id=UnitId.TERRAN_MARINE,
                _hitpoints=100,
                _shieldpoints=100,
                _armorpoints=100,
                _build_time=100,
                _mineral_cost=100,
                _gas_cost=100,
                _custom_unit_name=RichString(_value="custom-terran-marine-name"),
                _weapons=[],
            )
        ]
    )
    return RichChk(_chk_sections=[empty_decoded_str, rich_unis])


def test_it_finds_all_rich_strings_in_rich_chk(rich_chk_with_new_rich_strings: RichChk):
    rich_strings = DecodedStrSectionRebuilder.find_all_rich_strings_in_rich_chk(
        rich_chk_with_new_rich_strings
    )
    assert rich_strings == [RichString(_value="custom-terran-marine-name")]


def test_integration_it_throws_if_multiple_decoded_str_sections():
    rich_chk = RichChk(
        _chk_sections=[
            DecodedStrSection(_number_of_strings=0, _string_offsets=[], _strings=[]),
            DecodedStrSection(_number_of_strings=0, _string_offsets=[], _strings=[]),
        ]
    )
    with pytest.raises(ValueError):
        DecodedStrSectionRebuilder.rebuild_str_section_from_rich_chk(rich_chk)


def test_integration_it_throws_if_no_decoded_str_section_found():
    rich_chk = RichChk(_chk_sections=[])
    with pytest.raises(ValueError):
        DecodedStrSectionRebuilder.rebuild_str_section_from_rich_chk(rich_chk)


def test_integration_it_rebuilds_decoded_str_section_with_new_rich_strings(
    decoded_str_section: DecodedStrSection, rich_unis_with_new_string: RichUnisSection
):
    assert _RICH_UNIS_NEWLY_ADDED_STRING not in decoded_str_section.strings
    rich_chk = RichChk(_chk_sections=[decoded_str_section, rich_unis_with_new_string])
    new_str = DecodedStrSectionRebuilder.rebuild_str_section_from_rich_chk(rich_chk)
    assert new_str != decoded_str_section
    for string_ in _EXPECTED_STRINGS_IN_DECODED_STR:
        assert string_ in new_str.strings
    assert _RICH_UNIS_NEWLY_ADDED_STRING in new_str.strings


def test_integration_str_is_unchanged_if_no_new_strings(
    decoded_str_section: DecodedStrSection,
    rich_unis_with_already_existing_string: RichUnisSection,
):
    str_rebuilder = DecodedStrSectionRebuilder()
    rich_chk = RichChk(
        _chk_sections=[decoded_str_section, rich_unis_with_already_existing_string]
    )
    new_str = str_rebuilder.rebuild_str_section_from_rich_chk(rich_chk)
    assert new_str == decoded_str_section
