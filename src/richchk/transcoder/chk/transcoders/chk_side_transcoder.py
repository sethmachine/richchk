"""Decode and encode SIDE - Player Races.

Not required. Validation: Must be size of 12 bytes.

u8[12]: One byte per player slot (0-11) designating the player's race.
"""

import struct
from io import BytesIO

from ....model.chk.side.decoded_side_section import DecodedSideSection
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder

_NUM_PLAYERS = 12


class ChkSideTranscoder(
    ChkSectionTranscoder[DecodedSideSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedSideSection.section_name(),
):
    def decode(self, chk_section_binary_data: bytes) -> DecodedSideSection:
        bytes_stream: BytesIO = BytesIO(chk_section_binary_data)
        player_races = [
            struct.unpack("B", bytes_stream.read(1))[0] for _ in range(_NUM_PLAYERS)
        ]
        return DecodedSideSection(_player_races=player_races)

    def _encode(self, decoded_chk_section: DecodedSideSection) -> bytes:
        return struct.pack(f"{_NUM_PLAYERS}B", *decoded_chk_section.player_races)
