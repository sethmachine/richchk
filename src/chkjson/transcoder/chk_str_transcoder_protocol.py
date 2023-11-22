"""

"""

from chkjson.model.chk.str.decoded_str_section import DecodedStrSection
from chkjson.transcoder.chk_section_transcoder_protocol import (
    ChkSectionTranscoderProtocol,
)


class ChkStrTranscoder(ChkSectionTranscoderProtocol):
    def decode(self, chk_section_binary_data: bytes) -> DecodedStrSection:
        return DecodedStrSection(1, [1], ["1"])
