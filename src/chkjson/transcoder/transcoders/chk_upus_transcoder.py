"""Decoded and encode UPUS - CUWP Slots Used.

Not Required.

This section goes along with the "UPRP" section. This section just indicates which of
the 64 unit properties slot are used.

u8[64]: 1 byte for each trigger unit properties slot

00 - Properties slot is unused

01 - Properties slot is used
"""

import struct
from io import BytesIO

from ...model.chk.upus.decoded_upus_section import DecodedUpusSection
from ...transcoder.chk_section_transcoder import ChkSectionTranscoder
from ...transcoder.chk_section_transcoder_factory import _RegistrableTranscoder


class ChkUpusTranscoder(
    ChkSectionTranscoder[DecodedUpusSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedUpusSection.section_name(),
):

    _NUM_CUWP_SLOTS = 64

    def decode(self, chk_section_binary_data: bytes) -> DecodedUpusSection:
        bytes_stream: BytesIO = BytesIO(chk_section_binary_data)
        cuwp_slots_used: list[int] = [
            struct.unpack("B", bytes_stream.read(1))[0]
            for _ in range(self._NUM_CUWP_SLOTS)
        ]
        return DecodedUpusSection(_cuwp_slots_used=cuwp_slots_used)

    def _encode(self, decoded_chk_section: DecodedUpusSection) -> bytes:
        return struct.pack(
            "{}B".format(self._NUM_CUWP_SLOTS), *decoded_chk_section.cuwp_slots_used
        )
