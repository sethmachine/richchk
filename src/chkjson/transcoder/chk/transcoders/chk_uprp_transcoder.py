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

from ....model.chk.uprp.decoded_cuwp_slot import DecodedCuwpSlot
from ....model.chk.uprp.decoded_uprp_section import DecodedUprpSection
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder


class ChkUprpTranscoder(
    ChkSectionTranscoder[DecodedUprpSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedUprpSection.section_name(),
):
    _NUM_CUWP_SLOTS = 64

    def decode(self, chk_section_binary_data: bytes) -> DecodedUprpSection:
        bytes_stream: BytesIO = BytesIO(chk_section_binary_data)
        cuwp_slots: list[DecodedCuwpSlot] = []
        for _ in range(self._NUM_CUWP_SLOTS):
            valid_special_properties_flags = struct.unpack("H", bytes_stream.read(2))[0]
            valid_unit_properties_flags = struct.unpack("H", bytes_stream.read(2))[0]
            owner_player = struct.unpack("B", bytes_stream.read(1))[0]
            hitpoints_percent = struct.unpack("B", bytes_stream.read(1))[0]
            shieldpoints_percent = struct.unpack("B", bytes_stream.read(1))[0]
            enerypoints_percent = struct.unpack("B", bytes_stream.read(1))[0]
            resource_amount = struct.unpack("I", bytes_stream.read(4))[0]
            units_in_hangar = struct.unpack("H", bytes_stream.read(2))[0]
            flags = struct.unpack("H", bytes_stream.read(2))[0]
            padding = struct.unpack("I", bytes_stream.read(4))[0]
            cuwp_slots.append(
                DecodedCuwpSlot(
                    _valid_special_properties_flags=valid_special_properties_flags,
                    _valid_unit_properties_flags=valid_unit_properties_flags,
                    _owner_player=owner_player,
                    _hitpoints_percentage=hitpoints_percent,
                    _shieldpoints_percentage=shieldpoints_percent,
                    _energypoints_percentage=enerypoints_percent,
                    _resource_amount=resource_amount,
                    _units_in_hangar=units_in_hangar,
                    _flags=flags,
                    _padding=padding,
                )
            )
        return DecodedUprpSection(_cuwp_slots=cuwp_slots)

    def _encode(self, decoded_chk_section: DecodedUprpSection) -> bytes:
        data: bytes = b""
        for cuwp in decoded_chk_section.cuwp_slots:
            data += struct.pack("H", cuwp.valid_special_properties_flags)
            data += struct.pack("H", cuwp.valid_unit_properties_flags)
            data += struct.pack("B", cuwp.owner_player)
            data += struct.pack("B", cuwp.hitpoints_percentage)
            data += struct.pack("B", cuwp.shieldpoints_percentage)
            data += struct.pack("B", cuwp.energypoints_percentage)
            data += struct.pack("I", cuwp.resource_amount)
            data += struct.pack("H", cuwp.units_in_hangar)
            data += struct.pack("H", cuwp.flags)
            data += struct.pack("I", cuwp.padding)
        return data
