"""Decode and encode OWNR - StarCraft Player Types.

Required for all versions and all game types. Validation: Must be size of 12 bytes.

u8[12]: One byte per player slot (0-11) designating the controller type.
"""

import struct
from io import BytesIO

from ....model.chk.ownr.decoded_ownr_section import DecodedOwnrSection
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder

_NUM_PLAYERS = 12


class ChkOwnrTranscoder(
    ChkSectionTranscoder[DecodedOwnrSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedOwnrSection.section_name(),
):
    def decode(self, chk_section_binary_data: bytes) -> DecodedOwnrSection:
        bytes_stream: BytesIO = BytesIO(chk_section_binary_data)
        player_controllers = [
            struct.unpack("B", bytes_stream.read(1))[0] for _ in range(_NUM_PLAYERS)
        ]
        return DecodedOwnrSection(_player_controllers=player_controllers)

    def _encode(self, decoded_chk_section: DecodedOwnrSection) -> bytes:
        return struct.pack(
            f"{_NUM_PLAYERS}B", *decoded_chk_section.player_controllers
        )
