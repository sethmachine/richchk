"""Decode and encode MASK - Fog of War.

Flat array of u8 values, one per map tile (width * height bytes total).
"""

import struct

from ....model.chk.mask.decoded_mask_section import DecodedMaskSection
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder


class ChkMaskTranscoder(
    ChkSectionTranscoder[DecodedMaskSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedMaskSection.section_name(),
):
    def decode(self, chk_section_binary_data: bytes) -> DecodedMaskSection:
        num_tiles = len(chk_section_binary_data)
        fog_data = struct.unpack(f"{num_tiles}B", chk_section_binary_data)
        return DecodedMaskSection(_fog_data=fog_data)

    def _encode(self, decoded_chk_section: DecodedMaskSection) -> bytes:
        fog_data = decoded_chk_section.fog_data
        return struct.pack(f"{len(fog_data)}B", *fog_data)
