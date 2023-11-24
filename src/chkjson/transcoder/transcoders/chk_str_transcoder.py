"""

"""

from chkjson.model.chk.str.decoded_str_section import DecodedStrSection
from chkjson.transcoder.chk_section_transcoder import ChkSectionTranscoder
from chkjson.transcoder.chk_section_transcoder_factory import _RegistrableTranscoder


class ChkStrTranscoder(
    ChkSectionTranscoder[DecodedStrSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedStrSection.section_name(),
):
    def decode(self, chk_section_binary_data: bytes) -> DecodedStrSection:
        return DecodedStrSection(1, [1], ["1"])

    def _encode(self, decoded_chk_section: DecodedStrSection) -> bytes:
        return b""
