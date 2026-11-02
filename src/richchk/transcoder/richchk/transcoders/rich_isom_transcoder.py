"""Decode and encode ISOM - Isometric Terrain.

Simple pass-through: the rich representation is identical to the decoded one.
"""


from ....model.chk.isom.decoded_isom_section import DecodedIsomSection
from ....model.richchk.isom.rich_isom_section import RichIsomSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)


class RichIsomTranscoder(
    RichChkSectionTranscoder[RichIsomSection, DecodedIsomSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedIsomSection.section_name(),
):
    def decode(
        self,
        decoded_chk_section: DecodedIsomSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichIsomSection:
        return RichIsomSection(_data=list(decoded_chk_section.data))

    def encode(
        self,
        rich_chk_section: RichIsomSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedIsomSection:
        result = DecodedIsomSection(_data=tuple(rich_chk_section.data))
        return result
