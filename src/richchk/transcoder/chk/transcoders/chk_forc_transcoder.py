"""Decode and encode FORC - Force Settings.

Not required. Total size: 20 bytes (or less; missing bytes default to 0).

u8[8]:  Force assignment per player slot (0-7); values 0-3 indicate which force. u16[4]:
String index of each force's name (4 forces); 0 means default name. u8[4]:  Property
flags per force.
"""

import struct
from io import BytesIO

from ....model.chk.forc.decoded_forc_section import DecodedForcSection
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder

_NUM_PLAYERS = 8
_NUM_FORCES = 4


class ChkForcTranscoder(
    ChkSectionTranscoder[DecodedForcSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedForcSection.section_name(),
):
    def decode(self, chk_section_binary_data: bytes) -> DecodedForcSection:
        bytes_stream: BytesIO = BytesIO(chk_section_binary_data)
        player_force_assignments = [
            struct.unpack("B", bytes_stream.read(1))[0] for _ in range(_NUM_PLAYERS)
        ]
        force_name_string_ids = [
            struct.unpack("H", bytes_stream.read(2))[0] for _ in range(_NUM_FORCES)
        ]
        force_flags = [
            struct.unpack("B", bytes_stream.read(1))[0] for _ in range(_NUM_FORCES)
        ]
        return DecodedForcSection(
            _player_force_assignments=player_force_assignments,
            _force_name_string_ids=force_name_string_ids,
            _force_flags=force_flags,
        )

    def _encode(self, decoded_chk_section: DecodedForcSection) -> bytes:
        data: bytes = b""
        data += struct.pack(
            f"{_NUM_PLAYERS}B", *decoded_chk_section.player_force_assignments
        )
        data += struct.pack(
            f"{_NUM_FORCES}H", *decoded_chk_section.force_name_string_ids
        )
        data += struct.pack(f"{_NUM_FORCES}B", *decoded_chk_section.force_flags)
        return data
