"""Decode and encode the MRGN section which contain all locations data.

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

import struct
from io import BytesIO

from ....model.chk.mrgn.decoded_location import DecodedLocation
from ....model.chk.mrgn.decoded_mrgn_section import DecodedMrgnSection
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder


class ChkMrgnTranscoder(
    ChkSectionTranscoder[DecodedMrgnSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedMrgnSection.section_name(),
):
    def decode(self, chk_section_binary_data: bytes) -> DecodedMrgnSection:
        bytes_stream: BytesIO = BytesIO(chk_section_binary_data)
        locations: list[DecodedLocation] = []
        index = 0
        while bytes_stream.tell() != len(chk_section_binary_data):
            left_x1 = struct.unpack("I", bytes_stream.read(4))[0]
            top_y1 = struct.unpack("I", bytes_stream.read(4))[0]
            right_x2 = struct.unpack("I", bytes_stream.read(4))[0]
            bottom_y2 = struct.unpack("I", bytes_stream.read(4))[0]
            string_id = struct.unpack("H", bytes_stream.read(2))[0]
            elevation_flags = struct.unpack("H", bytes_stream.read(2))[0]
            locations.append(
                DecodedLocation(
                    _left_x1=left_x1,
                    _top_y1=top_y1,
                    _right_x2=right_x2,
                    _bottom_y2=bottom_y2,
                    _string_id=string_id,
                    _elevation_flags=elevation_flags,
                )
            )
            index += 1
        return DecodedMrgnSection(_locations=locations)

    def _encode(self, decoded_chk_section: DecodedMrgnSection) -> bytes:
        data: bytes = b""
        for location in decoded_chk_section.locations:
            data += struct.pack("I", location.left_x1)
            data += struct.pack("I", location.top_y1)
            data += struct.pack("I", location.right_x2)
            data += struct.pack("I", location.bottom_y2)
            data += struct.pack("H", location.string_id)
            data += struct.pack("H", location.elevation_flags)
        return data
