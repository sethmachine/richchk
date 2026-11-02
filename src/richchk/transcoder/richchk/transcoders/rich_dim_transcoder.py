"""Decode DIM."""

from ....model.chk.dim.decoded_dim_section import DecodedDimSection
from ....model.richchk.dim.rich_dim_section import RichDimSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)
from ....util import logger


class RichDimTranscoder(
    RichChkSectionTranscoder[RichDimSection, DecodedDimSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedDimSection.section_name(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(RichDimTranscoder.__name__)

    def decode(
        self,
        decoded_chk_section: DecodedDimSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichDimSection:
        return RichDimSection(
            _width=decoded_chk_section.width,
            _height=decoded_chk_section.height,
        )

    def encode(
        self,
        rich_chk_section: RichDimSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedDimSection:
        result = DecodedDimSection(
            _width=rich_chk_section.width,
            _height=rich_chk_section.height,
        )
        return result
