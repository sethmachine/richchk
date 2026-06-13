"""Decode and encode ERA - Tileset.

Required for all versions and all game types. Validation: Must be size of 2 bytes.

This section identifies the tileset of the scenario.

u16: Tileset index (0-7):

0 - Badlands

1 - Space Platform

2 - Installation

3 - Ashworld

4 - Jungle

5 - Desert

6 - Ice

7 - Twilight
"""

import struct
from io import BytesIO

from ....model.chk.era.decoded_era_section import DecodedEraSection
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder


class ChkEraTranscoder(
    ChkSectionTranscoder[DecodedEraSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedEraSection.section_name(),
):
    def decode(self, chk_section_binary_data: bytes) -> DecodedEraSection:
        bytes_stream: BytesIO = BytesIO(chk_section_binary_data)
        tileset = struct.unpack("H", bytes_stream.read(2))[0]
        return DecodedEraSection(_tileset=tileset)

    def _encode(self, decoded_chk_section: DecodedEraSection) -> bytes:
        return struct.pack("H", decoded_chk_section.tileset)
