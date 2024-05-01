""""""
import uuid
from typing import Optional

from chkjson.model.chk.mrgn.decoded_location import DecodedLocation
from chkjson.model.richchk.mrgn.rich_location import RichLocation
from chkjson.model.richchk.str.rich_string import RichString
from chkjson.transcoder.richchk.transcoders.richchk_mrgn_transcoder import (
    RichChkMrgnTranscoder,
)


def generate_unused_decoded_location() -> DecodedLocation:
    return DecodedLocation(
        _left_x1=0,
        _top_y1=0,
        _right_x2=0,
        _bottom_y2=0,
        _string_id=0,
        _elevation_flags=0,
    )


def generate_decoded_location() -> DecodedLocation:
    return DecodedLocation(
        _left_x1=100,
        _top_y1=200,
        _right_x2=300,
        _bottom_y2=400,
        _string_id=500,
        _elevation_flags=56,
    )


def generate_decoded_location_with_elevation_flags(
    elevation_flags: int,
) -> DecodedLocation:
    return DecodedLocation(
        _left_x1=100,
        _top_y1=200,
        _right_x2=300,
        _bottom_y2=400,
        _string_id=500,
        _elevation_flags=elevation_flags,
    )


def generate_rich_location(index: Optional[int] = None):
    return RichLocation(
        _left_x1=100,
        _top_y1=200,
        _right_x2=300,
        _bottom_y2=400,
        _custom_location_name=RichString(_value=f"location {uuid.uuid4()}"),
        _index=index,
    )


def generate_rich_location_with_all_elevations_enabled(
    custom_name: RichString, index: int
) -> RichLocation:
    return RichLocation(
        _left_x1=100,
        _top_y1=200,
        _right_x2=300,
        _bottom_y2=400,
        _custom_location_name=custom_name,
        _index=index,
    )


def generate_rich_location_with_all_elevations_disabled(
    custom_name: RichString, index: int
) -> RichLocation:
    return RichLocation(
        _left_x1=100,
        _top_y1=200,
        _right_x2=300,
        _bottom_y2=400,
        _custom_location_name=custom_name,
        _index=index,
        _low_elevation=False,
        _medium_elevation=False,
        _high_elevation=False,
        _low_air=False,
        _medium_air=False,
        _high_air=False,
    )


def compare_decoded_and_rich_location(
    decoded: DecodedLocation, rich: RichLocation
) -> bool:
    return (
        (decoded.top_y1 == rich.top_y1)
        and (decoded.bottom_y2 == rich.bottom_y2)
        and (decoded.left_x1 == rich.left_x1)
        and (decoded.right_x2 == rich.right_x2)
        and (
            decoded.elevation_flags
            == RichChkMrgnTranscoder._encode_elevation_flags(rich)
        )
    )
