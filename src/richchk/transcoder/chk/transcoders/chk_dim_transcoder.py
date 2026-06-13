"""Decode and encode DIM - Map Dimensions.

Required for all versions and all game types. Validation: Must be size of 4 bytes.

This section specifies the width and height of the map in tiles.

u16: Width of the map in tiles

u16: Height of the map in tiles
"""

import struct
from io import BytesIO

from ....model.chk.dim.decoded_dim_section import DecodedDimSection
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder


class ChkDimTranscoder(
    ChkSectionTranscoder[DecodedDimSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedDimSection.section_name(),
):
    def decode(self, chk_section_binary_data: bytes) -> DecodedDimSection:
        bytes_stream: BytesIO = BytesIO(chk_section_binary_data)
        width = struct.unpack("H", bytes_stream.read(2))[0]
        height = struct.unpack("H", bytes_stream.read(2))[0]
        return DecodedDimSection(_width=width, _height=height)

    def _encode(self, decoded_chk_section: DecodedDimSection) -> bytes:
        data: bytes = b""
        data += struct.pack("H", decoded_chk_section.width)
        data += struct.pack("H", decoded_chk_section.height)
        return data
