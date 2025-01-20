import pytest

from richchk.io.richchk.rich_str_lookup_builder import RichStrLookupBuilder
from richchk.model.chk.decoded_string_section import DecodedStringSection
from richchk.model.chk.str.decoded_str_section import DecodedStrSection
from richchk.model.chk.strx.decoded_strx_section import DecodedStrxSection
from richchk.model.richchk.str.rich_str_lookup import RichStrLookup
from richchk.model.richchk.str.rich_string import RichString
from richchk.transcoder.chk.transcoders.chk_str_transcoder import ChkStrTranscoder
from richchk.transcoder.chk.transcoders.chk_strx_transcoder import ChkStrxTranscoder

from ...chk_resources import CHK_SECTION_FILE_PATHS

# these strings were added into the CHK section by using a GUI map editor
_EXPECTED_STRINGS_WITH_ID = [
    {"string": "test-string-1-marine", "id": 8},
    {"string": "test-string-2-firebat", "id": 9},
    {"string": "test-string-3-ghost", "id": 10},
]


@pytest.fixture(scope="function")
def str_section() -> DecodedStrSection:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedStrSection.section_name().value], "rb"
    ) as f:
        return ChkStrTranscoder().decode(f.read())


@pytest.fixture(scope="function")
def strx_section() -> DecodedStrxSection:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedStrxSection.section_name().value], "rb"
    ) as f:
        return ChkStrxTranscoder().decode(f.read())


def test_it_builds_lookup_for_str(str_section):
    lookup_builder: RichStrLookupBuilder = RichStrLookupBuilder()
    lookup_builder.build_lookup(str_section)


def test_it_builds_lookup_for_strx(strx_section):
    lookup_builder: RichStrLookupBuilder = RichStrLookupBuilder()
    lookup_builder.build_lookup(strx_section)


def test_it_builds_lookup_with_expected_structure_for_str(str_section):
    lookup_builder: RichStrLookupBuilder = RichStrLookupBuilder()
    lookup: RichStrLookup = lookup_builder.build_lookup(str_section)
    assert len(lookup._string_by_id_lookup) == len(str_section.strings_offsets)
    for expected_string in _EXPECTED_STRINGS_WITH_ID:
        assert lookup.get_string_by_id(expected_string["id"]) == RichString(
            _value=expected_string["string"]
        )
        assert (
            lookup.get_id_by_string(RichString(_value=expected_string["string"]))
            == expected_string["id"]
        )


def test_it_builds_lookup_with_expected_structure_for_strx(strx_section):
    lookup_builder: RichStrLookupBuilder = RichStrLookupBuilder()
    lookup: RichStrLookup = lookup_builder.build_lookup(strx_section)
    assert len(lookup._string_by_id_lookup) == len(strx_section.strings_offsets)
    for expected_string in _EXPECTED_STRINGS_WITH_ID:
        assert lookup.get_string_by_id(expected_string["id"]) == RichString(
            _value=expected_string["string"]
        )
        assert (
            lookup.get_id_by_string(RichString(_value=expected_string["string"]))
            == expected_string["id"]
        )


def test_it_throws_if_string_section_is_not_str_or_strx():
    class UnknownStringSection(DecodedStringSection):
        @property
        def number_of_strings(self) -> int:
            return 0

        @property
        def strings_offsets(self) -> list[int]:
            return []

        @property
        def strings(self) -> list[str]:
            return []

    with pytest.raises(ValueError):
        RichStrLookupBuilder().build_lookup(UnknownStringSection())
