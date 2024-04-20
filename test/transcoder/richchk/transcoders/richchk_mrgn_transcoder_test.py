import pytest

from chkjson.model.chk.mrgn.decoded_location import DecodedLocation
from chkjson.model.chk.mrgn.decoded_mrgn_section import DecodedMrgnSection
from chkjson.model.richchk.mrgn.rich_location import RichLocation
from chkjson.model.richchk.mrgn.rich_mrgn_section import RichMrgnSection
from chkjson.model.richchk.richchk_decode_context import RichChkDecodeContext
from chkjson.model.richchk.richchk_encode_context import RichChkEncodeContext
from chkjson.model.richchk.str.rich_str_lookup import RichStrLookup
from chkjson.model.richchk.str.rich_string import RichNullString, RichString
from chkjson.transcoder.chk.transcoders.chk_mrgn_transcoder import ChkMrgnTranscoder
from chkjson.transcoder.richchk.transcoders.richchk_mrgn_transcoder import (
    RichChkMrgnTranscoder,
)

from ....chk_resources import CHK_SECTION_FILE_PATHS
from ....fixtures.location_fixtures import (
    generate_decoded_location,
    generate_decoded_location_with_elevation_flags,
    generate_rich_location_with_all_elevations_disabled,
    generate_rich_location_with_all_elevations_enabled,
    generate_unused_decoded_location,
)
from ....fixtures.richchk_io_fixtures import generate_empty_rich_chk_decode_context

# a "Location 0" was made with the following data in a GUI editor
_EXPECTED_LOCATION_LEFT = 192
_EXPECTED_LOCATION_TOP = 288
_EXPECTED_LOCATION_RIGHT = 384
_EXPECTED_LOCATION_BOTTOM = 448
# corresponds to disabling low, med, high air checks: 0000000000111000
_EXPECTED_LOCATION_ELEVATION_FLAGS = 56
# location 0 has a string ID of 11
_LOCATION_ZERO_STRING_ID = 11
_LOCATION_ZERO_INDEX = 0
_LOCATION_ZERO_STRING_VALUE = "LOCATION ZERO"
_LOCATION_ANYWHERE_STRING_VALUE = "Anywhere"
_LOCATION_ANYWHERE_STRING_ID = 3


@pytest.fixture
def real_decoded_mrgn() -> DecodedMrgnSection:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedMrgnSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return ChkMrgnTranscoder().decode(chk_binary_data)


def test_integration_it_decodes_expected_rich_location(real_decoded_mrgn):
    rich_transcoder = RichChkMrgnTranscoder()
    rich_mrgn = rich_transcoder.decode(
        real_decoded_mrgn,
        rich_chk_decode_context=RichChkDecodeContext(
            _rich_str_lookup=RichStrLookup(
                _string_by_id_lookup={
                    _LOCATION_ZERO_STRING_ID: RichString(
                        _value=_LOCATION_ZERO_STRING_VALUE
                    )
                },
                _id_by_string_lookup={},
            )
        ),
    )
    rich_location: RichLocation = rich_mrgn.locations[0]
    assert rich_location.left_x1 == _EXPECTED_LOCATION_LEFT
    assert rich_location.top_y1 == _EXPECTED_LOCATION_TOP
    assert rich_location.right_x2 == _EXPECTED_LOCATION_RIGHT
    assert rich_location.bottom_y2 == _EXPECTED_LOCATION_BOTTOM
    assert rich_location.custom_location_name == RichString(
        _value=_LOCATION_ZERO_STRING_VALUE
    )
    assert rich_location.index == _LOCATION_ZERO_INDEX
    assert rich_location.low_elevation
    assert rich_location.medium_elevation
    assert rich_location.high_elevation
    assert not rich_location.low_air
    assert not rich_location.medium_air
    assert not rich_location.high_air


def test_it_does_not_include_empty_locations_in_rich_mrgn():
    expected_decoded_location = generate_decoded_location()
    decoded_mrgn = DecodedMrgnSection(
        _locations=[generate_unused_decoded_location(), expected_decoded_location]
    )
    rich_transcoder = RichChkMrgnTranscoder()
    rich_mrgn = rich_transcoder.decode(
        decoded_mrgn, rich_chk_decode_context=generate_empty_rich_chk_decode_context()
    )
    assert len(rich_mrgn.locations) == 1
    only_location = rich_mrgn.locations[0]
    assert only_location.left_x1 == expected_decoded_location.left_x1
    assert only_location.top_y1 == expected_decoded_location.top_y1
    assert only_location.right_x2 == expected_decoded_location.right_x2
    assert only_location.bottom_y2 == expected_decoded_location.bottom_y2
    assert only_location.custom_location_name == RichNullString()
    # the "empty" location occupies index 0
    assert only_location.index == 1


def test_it_decodes_elevation_flags():
    decoded_mrgn = DecodedMrgnSection(
        _locations=[
            generate_decoded_location_with_elevation_flags(0),
            # first bit (low elevation) is disabled
            generate_decoded_location_with_elevation_flags(1),
            # all 6 bits are set/disabled
            generate_decoded_location_with_elevation_flags(63),
            # every other flag is disabled: 010101
            generate_decoded_location_with_elevation_flags(21),
        ]
    )
    rich_transcoder = RichChkMrgnTranscoder()
    rich_mrgn = rich_transcoder.decode(
        decoded_mrgn, rich_chk_decode_context=generate_empty_rich_chk_decode_context()
    )
    assert len(rich_mrgn.locations) == 4
    assert (
        rich_mrgn.locations[0].low_elevation
        and rich_mrgn.locations[0].medium_elevation
        and rich_mrgn.locations[0].high_elevation
        and rich_mrgn.locations[0].low_air
        and rich_mrgn.locations[0].medium_air
        and rich_mrgn.locations[0].high_air
    )
    assert (
        not rich_mrgn.locations[1].low_elevation
        and rich_mrgn.locations[1].medium_elevation
        and rich_mrgn.locations[1].high_elevation
        and rich_mrgn.locations[1].low_air
        and rich_mrgn.locations[1].medium_air
        and rich_mrgn.locations[1].high_air
    )
    assert (
        not rich_mrgn.locations[2].low_elevation
        and not rich_mrgn.locations[2].medium_elevation
        and not rich_mrgn.locations[2].high_elevation
        and not rich_mrgn.locations[2].low_air
        and not rich_mrgn.locations[2].medium_air
        and not rich_mrgn.locations[2].high_air
    )
    assert (
        not rich_mrgn.locations[3].low_elevation
        and rich_mrgn.locations[3].medium_elevation
        and not rich_mrgn.locations[3].high_elevation
        and rich_mrgn.locations[3].low_air
        and not rich_mrgn.locations[3].medium_air
        and rich_mrgn.locations[3].high_air
    )


def test_integration_it_encodes_back_to_expected_decoded_location():
    rich_mrgn = RichMrgnSection(
        _locations=[
            generate_rich_location_with_all_elevations_enabled(
                RichString(_value="foo"), 55
            ),
            generate_rich_location_with_all_elevations_disabled(
                RichString(_value="bar"), 56
            ),
        ]
    )
    rich_transcoder = RichChkMrgnTranscoder()
    decoded_mrgn = rich_transcoder.encode(
        rich_mrgn,
        rich_chk_encode_context=RichChkEncodeContext(
            _rich_str_lookup=RichStrLookup(
                _string_by_id_lookup={},
                _id_by_string_lookup={"foo": 0, "bar": 1},
            )
        ),
    )

    expected_decoded_location_with_all_elevation_flags_enabled = DecodedLocation(
        _left_x1=rich_mrgn.locations[0].left_x1,
        _top_y1=rich_mrgn.locations[0].top_y1,
        _right_x2=rich_mrgn.locations[0].right_x2,
        _bottom_y2=rich_mrgn.locations[0].bottom_y2,
        _string_id=0,
        _elevation_flags=0,
    )

    expected_decoded_location_with_all_elevation_flags_disabled = DecodedLocation(
        _left_x1=rich_mrgn.locations[1].left_x1,
        _top_y1=rich_mrgn.locations[1].top_y1,
        _right_x2=rich_mrgn.locations[1].right_x2,
        _bottom_y2=rich_mrgn.locations[1].bottom_y2,
        _string_id=1,
        # 63 in decimal is 111111 in binary, which is all elevation flags disabled
        _elevation_flags=63,
    )

    assert (
        expected_decoded_location_with_all_elevation_flags_enabled
        in decoded_mrgn.locations
    )
    assert (
        expected_decoded_location_with_all_elevation_flags_disabled
        in decoded_mrgn.locations
    )


def test_integration_it_decodes_and_encodes_back_to_chk_without_changing_data(
    real_decoded_mrgn,
):
    rich_chk_decode_context = RichChkDecodeContext(
        _rich_str_lookup=RichStrLookup(
            _string_by_id_lookup={
                _LOCATION_ZERO_STRING_ID: RichString(
                    _value=_LOCATION_ZERO_STRING_VALUE
                ),
                _LOCATION_ANYWHERE_STRING_ID: RichString(
                    _value=_LOCATION_ANYWHERE_STRING_VALUE
                ),
            },
            _id_by_string_lookup={},
        )
    )
    rich_chk_encode_context = RichChkEncodeContext(
        _rich_str_lookup=RichStrLookup(
            _string_by_id_lookup={},
            _id_by_string_lookup={
                _LOCATION_ZERO_STRING_VALUE: _LOCATION_ZERO_STRING_ID,
                _LOCATION_ANYWHERE_STRING_VALUE: _LOCATION_ANYWHERE_STRING_ID,
            },
        )
    )
    rich_transcoder = RichChkMrgnTranscoder()
    rich_mrgn = rich_transcoder.decode(
        real_decoded_mrgn,
        rich_chk_decode_context=rich_chk_decode_context,
    )

    actual_decoded_mrgn = rich_transcoder.encode(
        rich_mrgn,
        rich_chk_encode_context=rich_chk_encode_context,
    )
    rich_mrgn_again = rich_transcoder.decode(
        actual_decoded_mrgn,
        rich_chk_decode_context=rich_chk_decode_context,
    )
    assert rich_mrgn == rich_mrgn_again
    # this test could fail because any non-semantic information
    # could be lost when decoding to a Rich representation
    # this includes unused elevation flags data, etc.
    # the actual MRGN has the original 64 locations only
    assert real_decoded_mrgn.locations[:64] == actual_decoded_mrgn.locations[:64]
