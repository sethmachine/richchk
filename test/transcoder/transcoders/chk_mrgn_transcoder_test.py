from chkjson.model.chk.mrgn.decoded_mrgn_section import DecodedMrgnSection
from chkjson.transcoder.chk.transcoders.chk_mrgn_transcoder import ChkMrgnTranscoder

from ...chk_resources import CHK_SECTION_FILE_PATHS

# a "Location 0" was made with the following data in a GUI editor
_EXPECTED_LOCATION_LEFT = 192
_EXPECTED_LOCATION_TOP = 288
_EXPECTED_LOCATION_RIGHT = 384
_EXPECTED_LOCATION_BOTTOM = 448
# corresponds to disabling low, med, high air checks: 0000000000111000
_EXPECTED_LOCATION_ELEVATION_FLAGS = 56


def _read_chk_section() -> bytes:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedMrgnSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return chk_binary_data


def test_it_decodes_expected_location():
    transcoder: ChkMrgnTranscoder = ChkMrgnTranscoder()
    chk_binary_data = _read_chk_section()
    mrgn_section: DecodedMrgnSection = transcoder.decode(chk_binary_data)
    location_zero = mrgn_section.locations[0]
    assert location_zero.left_x1 == _EXPECTED_LOCATION_LEFT
    assert location_zero.top_y1 == _EXPECTED_LOCATION_TOP
    assert location_zero.right_x2 == _EXPECTED_LOCATION_RIGHT
    assert location_zero.bottom_y2 == _EXPECTED_LOCATION_BOTTOM
    assert location_zero.elevation_flags == _EXPECTED_LOCATION_ELEVATION_FLAGS


def test_it_decodes_and_encodes_without_changing_data():
    transcoder: ChkMrgnTranscoder = ChkMrgnTranscoder()
    chk_binary_data = _read_chk_section()
    mrgn_section: DecodedMrgnSection = transcoder.decode(chk_binary_data)
    actual_encoded_data = transcoder.encode(mrgn_section, include_header=False)
    assert actual_encoded_data == chk_binary_data
    assert transcoder.decode(actual_encoded_data) == transcoder.decode(chk_binary_data)
