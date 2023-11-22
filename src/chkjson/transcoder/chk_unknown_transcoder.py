"""

"""

from chkjson.model.chk.unknown.decoded_unknown_section import DecodedUnknownSection
from chkjson.transcoder.chk_section_transcoder import ChkSectionTranscoder


class ChkUnknownTranscoder(ChkSectionTranscoder[DecodedUnknownSection]):
    def decode(self, chk_section_binary_data: bytes) -> DecodedUnknownSection:
        return DecodedUnknownSection("unknown", b"")

    def _encode(self, decoded_chk_section: DecodedUnknownSection) -> bytes:
        return b""
