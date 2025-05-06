"""Decoded and encode VER - File Format Version.

Required for all versions and all game types. Validation: Must be size of 2 bytes.

This section identifies the file format version.

u16: File format version:

59 - Starcraft 1.00 (original retail release)

63 - Starcraft 1.04 (hybrid)

64 - Starcraft Remastered (1.21) (hybrid)

205 - Brood War 1.00 (1.04)

206 - Starcraft Remastered (1.21) (broodwar)

 This is the only version code section to actually be read by StarCraft (of TYPE, VER ,
IVER, and IVE2). Any other value is invalid in retail StarCraft and is usually a beta
version.

Other unsupported versions include:

17 - Warcraft II retail (.PUD)

19 - Warcraft II Expansion (.PUD)

47 - Starcraft Beta

57 - Starcraft Prerelease

61 - Brood War internal (map version 61)

75 - Brood War internal (map version 75) (Broodwar Battle.net Beta)

201 - Brood War internal (map version 201)

203 - Brood War internal (map version 203)
"""

import struct
from io import BytesIO

from ....model.chk.ver.decoded_ver_section import DecodedVerSection
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder


class ChkVerTranscoder(
    ChkSectionTranscoder[DecodedVerSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedVerSection.section_name(),
):
    def decode(self, chk_section_binary_data: bytes) -> DecodedVerSection:
        bytes_stream: BytesIO = BytesIO(chk_section_binary_data)
        version = struct.unpack("H", bytes_stream.read(2))[0]
        return DecodedVerSection(_version=version)

    def _encode(self, decoded_chk_section: DecodedVerSection) -> bytes:
        return struct.pack("H", decoded_chk_section.version)
