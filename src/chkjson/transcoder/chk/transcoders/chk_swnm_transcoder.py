"""Decode and encode the SWNM section which contain switch names data.

Not Required.

This section contains the strings used for each switch. There are 256 switches, and
can't be any more or any less.

u32[256]: One long for each switch, specifies the string number for the name of each
switch. Unnamed switches will have an index of 0, and have a default switch name.
"""

import struct
from io import BytesIO

from ....model.chk.swnm.decoded_swnm_section import DecodedSwnmSection
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder


class ChkSwnmTranscoder(
    ChkSectionTranscoder[DecodedSwnmSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedSwnmSection.section_name(),
):
    NUM_SWITCHES = 256

    def decode(self, chk_section_binary_data: bytes) -> DecodedSwnmSection:
        bytes_stream: BytesIO = BytesIO(chk_section_binary_data)
        string_ids = [
            struct.unpack("I", bytes_stream.read(4))[0]
            for _ in range(self.NUM_SWITCHES)
        ]
        return DecodedSwnmSection(_switch_string_ids=string_ids)

    def _encode(self, decoded_chk_section: DecodedSwnmSection) -> bytes:
        data: bytes = b""
        data += struct.pack(
            "{}I".format(self.NUM_SWITCHES), *decoded_chk_section.switch_string_ids
        )
        return data
