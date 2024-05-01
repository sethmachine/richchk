"""Decode the MRGN - Locations section.

Required for all versions. Not required for Melee. Validation: 1280 bytes for retail,
5100 bytes for Hybrid and Broodwar.

This section contains all the locations that the map uses. In a vanilla map, this
section contains 64 locations. In a Hybrid or Brood War map, this section will expand to
contain 255 locations.

Each location gets one of the following location entries. The 'Anywhere' location, is
ALWAYS location 64.

u32: Left (X1) coordinate of location, in pixels (usually 32 pt grid aligned)

u32: Top (Y1) coordinate of location, in pixels

u32: Right (X2) coordinate of location, in pixels

u32: Bottom (Y2) coordinate of location, in pixels

u16: String number of the name of this location

u16: Location elevation flags. If an elevation is disabled in the location, it's bit
will be on (1)

Bit 0 - Low elevation

Bit 1 - Medium elevation

Bit 2 - High elevation

Bit 3 - Low air

Bit 4 - Medium air

Bit 5 - High air

Bit 6-15 - Unused

Note that in typical locations Right is always larger than Left and Bottom is always
larger than Top. However, you can reverse one or both of these for Inverted Locations.
"""

import dataclasses
from typing import Optional

from ....model.chk.mrgn.decoded_location import DecodedLocation
from ....model.chk.mrgn.decoded_mrgn_section import DecodedMrgnSection
from ....model.richchk.mrgn.rich_location import RichLocation
from ....model.richchk.mrgn.rich_mrgn_section import RichMrgnSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)
from ....util import logger


@dataclasses.dataclass(frozen=True)
class _LocationElevationFlags:
    low_elevation: bool = True
    medium_elevation: bool = True
    high_elevation: bool = True
    low_air: bool = True
    medium_air: bool = True
    high_air: bool = True


class RichChkMrgnTranscoder(
    RichChkSectionTranscoder[RichMrgnSection, DecodedMrgnSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedMrgnSection.section_name(),
):
    # location index 63 is always reserved for "Anywhere"
    _MAX_LOCATIONS = 255

    def __init__(self) -> None:
        self.log = logger.get_logger(RichChkMrgnTranscoder.__name__)

    def decode(
        self,
        decoded_chk_section: DecodedMrgnSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichMrgnSection:
        locations: list[RichLocation] = []
        loc_index = 0
        for decoded_location in decoded_chk_section.locations:
            if not self._is_unused_decoded_location(decoded_location):
                elevation_flags = self._decode_elevation_flags(
                    decoded_location=decoded_location
                )
                locations.append(
                    RichLocation(
                        _left_x1=decoded_location.left_x1,
                        _top_y1=decoded_location.top_y1,
                        _right_x2=decoded_location.right_x2,
                        _bottom_y2=decoded_location.bottom_y2,
                        _custom_location_name=rich_chk_decode_context.rich_str_lookup.get_string_by_id(
                            decoded_location.string_id
                        ),
                        _index=loc_index + 1,
                        _low_elevation=elevation_flags.low_elevation,
                        _medium_elevation=elevation_flags.medium_elevation,
                        _high_elevation=elevation_flags.high_elevation,
                        _low_air=elevation_flags.low_air,
                        _medium_air=elevation_flags.medium_air,
                        _high_air=elevation_flags.high_air,
                    )
                )
            loc_index += 1
        return RichMrgnSection(_locations=locations)

    @classmethod
    def _is_unused_decoded_location(cls, decoded_location: DecodedLocation) -> bool:
        """Filter out empty/placeholder locations from the DecodedMrgnSection.

        :param decoded_location:
        :return:
        """
        return (
            decoded_location.left_x1 == 0
            and decoded_location.top_y1 == 0
            and decoded_location.right_x2 == 0
            and decoded_location.bottom_y2 == 0
            and decoded_location.string_id == 0
            and decoded_location.elevation_flags == 0
        )

    @classmethod
    def _decode_elevation_flags(
        cls, decoded_location: DecodedLocation
    ) -> _LocationElevationFlags:
        elevation_flags_bit_string = "{:016b}".format(decoded_location.elevation_flags)
        # Starcraft bit string is read right to left, so the first bit
        # is the last position in the bit string, etc.
        # bit of 1 means the elevation is disabled, 0 is enabled
        return _LocationElevationFlags(
            low_elevation=not bool(int(elevation_flags_bit_string[-1])),
            medium_elevation=not bool(int(elevation_flags_bit_string[-2])),
            high_elevation=not bool(int(elevation_flags_bit_string[-3])),
            low_air=not bool(int(elevation_flags_bit_string[-4])),
            medium_air=not bool(int(elevation_flags_bit_string[-5])),
            high_air=not bool(int(elevation_flags_bit_string[-6])),
        )

    @classmethod
    def _encode_elevation_flags(cls, rich_location: RichLocation) -> int:
        return int(
            f"{int((not rich_location.high_air))}"
            f"{int((not rich_location.medium_air))}"
            f"{int((not rich_location.low_air))}"
            f"{int((not rich_location.high_elevation))}"
            f"{int((not rich_location.medium_elevation))}"
            f"{int((not rich_location.low_elevation))}",
            base=2,
        )

    def encode(
        self,
        rich_chk_section: RichMrgnSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedMrgnSection:
        # TODO: need to build the location index map before hand!  assign locations without indices an index
        # can be done in the RichChkEncodeContext generation step
        # subtract 1 to get zero index used for array storage
        location_by_index = {
            x.index - 1: x for x in rich_chk_section.locations if x.index is not None
        }
        decoded_locations: list[DecodedLocation] = []
        for location_index_in_decoded_mrgn in range(0, self._MAX_LOCATIONS):
            maybe_location: Optional[RichLocation] = location_by_index.get(
                location_index_in_decoded_mrgn, None
            )
            if not maybe_location:
                decoded_locations.append(self._generate_unused_decoded_location())
            else:
                decoded_locations.append(
                    self._encode_rich_location(maybe_location, rich_chk_encode_context)
                )
        return DecodedMrgnSection(_locations=decoded_locations)

    @classmethod
    def _encode_rich_location(
        cls, rich_location: RichLocation, rich_chk_encode_context: RichChkEncodeContext
    ) -> DecodedLocation:
        return DecodedLocation(
            _left_x1=rich_location.left_x1,
            _top_y1=rich_location.top_y1,
            _right_x2=rich_location.right_x2,
            _bottom_y2=rich_location.bottom_y2,
            _string_id=rich_chk_encode_context.rich_str_lookup.get_id_by_string(
                rich_string=rich_location.custom_location_name
            ),
            _elevation_flags=cls._encode_elevation_flags(rich_location),
        )

    @classmethod
    def _generate_unused_decoded_location(cls) -> DecodedLocation:
        """Generate filler location data to fill in any unused locations."""
        return DecodedLocation(
            _left_x1=0,
            _top_y1=0,
            _right_x2=0,
            _bottom_y2=0,
            _string_id=0,
            _elevation_flags=0,
        )
