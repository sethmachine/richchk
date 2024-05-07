"""Decode the TRIG - Triggers section."""

from ....model.chk.trig.decoded_trig_section import DecodedTrigSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....model.richchk.trig.rich_trig_section import RichTrigSection
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)
from ....util import logger


class RichChkTrigTranscoder(
    RichChkSectionTranscoder[RichTrigSection, DecodedTrigSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedTrigSection.section_name(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(RichChkTrigTranscoder.__name__)

    def decode(
        self,
        decoded_chk_section: DecodedTrigSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichTrigSection:
        return RichTrigSection(_triggers=decoded_chk_section.triggers)

    def encode(
        self,
        rich_chk_section: RichTrigSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTrigSection:
        return DecodedTrigSection(_triggers=rich_chk_section.triggers)
