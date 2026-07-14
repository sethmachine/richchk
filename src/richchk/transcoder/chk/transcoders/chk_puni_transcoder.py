"""Decode and encode PUNI - Player Unit Restrictions.

u8[12][228] player_unit_availability u8[228]     global_unit_availability u8[12][228]
player_uses_defaults

Total: 5700 bytes.
"""

import struct
from io import BytesIO

from ....model.chk.puni.decoded_puni_section import DecodedPuniSection
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder

_NUM_PLAYERS = 12
_NUM_UNITS = 228
_PLAYER_UNITS_SIZE = _NUM_PLAYERS * _NUM_UNITS


class ChkPuniTranscoder(
    ChkSectionTranscoder[DecodedPuniSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedPuniSection.section_name(),
):
    def decode(self, chk_section_binary_data: bytes) -> DecodedPuniSection:
        bytes_stream: BytesIO = BytesIO(chk_section_binary_data)
        player_unit_availability = list(
            struct.unpack(
                f"{_PLAYER_UNITS_SIZE}B", bytes_stream.read(_PLAYER_UNITS_SIZE)
            )
        )
        global_unit_availability = list(
            struct.unpack(f"{_NUM_UNITS}B", bytes_stream.read(_NUM_UNITS))
        )
        player_uses_defaults = list(
            struct.unpack(
                f"{_PLAYER_UNITS_SIZE}B", bytes_stream.read(_PLAYER_UNITS_SIZE)
            )
        )
        return DecodedPuniSection(
            _player_unit_availability=player_unit_availability,
            _global_unit_availability=global_unit_availability,
            _player_uses_defaults=player_uses_defaults,
        )

    def _encode(self, decoded_chk_section: DecodedPuniSection) -> bytes:
        data = struct.pack(
            f"{_PLAYER_UNITS_SIZE}B",
            *decoded_chk_section.player_unit_availability,
        )
        data += struct.pack(
            f"{_NUM_UNITS}B",
            *decoded_chk_section.global_unit_availability,
        )
        data += struct.pack(
            f"{_PLAYER_UNITS_SIZE}B",
            *decoded_chk_section.player_uses_defaults,
        )
        return data
