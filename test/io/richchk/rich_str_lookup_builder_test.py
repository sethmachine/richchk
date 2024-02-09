from chkjson.io.richchk.rich_str_lookup_builder import RichStrLookupBuilder
from chkjson.model.chk.str.decoded_str_section import DecodedStrSection
from chkjson.model.richchk.str.rich_str_lookup import RichStrLookup
from chkjson.model.richchk.str.rich_string import RichString
from chkjson.transcoder.chk.transcoders.chk_str_transcoder import ChkStrTranscoder

from ...chk_resources import CHK_SECTION_FILE_PATHS

# these strings were added into the CHK section by using a GUI map editor
_EXPECTED_STRINGS_WITH_ID = [
    {"string": "test-string-1-marine", "id": 8},
    {"string": "test-string-2-firebat", "id": 9},
    {"string": "test-string-3-ghost", "id": 10},
]


def _read_chk_section() -> bytes:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedStrSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return chk_binary_data


def test_it_builds_lookup():
    transcoder: ChkStrTranscoder = ChkStrTranscoder()
    lookup_builder: RichStrLookupBuilder = RichStrLookupBuilder()
    chk_binary_data = _read_chk_section()
    str_section: DecodedStrSection = transcoder.decode(chk_binary_data)
    lookup_builder.build_lookup(str_section)


def test_it_builds_lookup_with_expected_structure():
    transcoder: ChkStrTranscoder = ChkStrTranscoder()
    lookup_builder: RichStrLookupBuilder = RichStrLookupBuilder()
    chk_binary_data = _read_chk_section()
    str_section: DecodedStrSection = transcoder.decode(chk_binary_data)
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
