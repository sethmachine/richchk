"""Decode and encode ISOM - Isometric Terrain.

Flat array of u16 values.  Total count is ((width/2 + 1) * (height + 1)) * 4.
"""

import struct

from ....model.chk.isom.decoded_isom_section import DecodedIsomSection
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder


class ChkIsomTranscoder(
    ChkSectionTranscoder[DecodedIsomSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedIsomSection.section_name(),
):
    def decode(self, chk_section_binary_data: bytes) -> DecodedIsomSection:
        num_values = len(chk_section_binary_data) // 2
        data = struct.unpack(f"{num_values}H", chk_section_binary_data)
        return DecodedIsomSection(_data=data)

    def _encode(self, decoded_chk_section: DecodedIsomSection) -> bytes:
        data = decoded_chk_section.data
        return struct.pack(f"{len(data)}H", *data)
