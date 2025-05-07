"""Decode VER.

VER must be valued 206 (STARCRAFT_REMASTERED_BROODWAR) in order to use STRx section.
"""
from ....model.chk.ver.decoded_ver_section import DecodedVerSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....model.richchk.ver.rich_ver_section import RichVerSection
from ....model.richchk.ver.ver_version import VerVersion
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)
from ....util import logger
from .helpers.richchk_enum_transcoder import RichChkEnumTranscoder


class RichVerTranscoder(
    RichChkSectionTranscoder[RichVerSection, DecodedVerSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedVerSection.section_name(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(RichVerTranscoder.__name__)

    def decode(
        self,
        decoded_chk_section: DecodedVerSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichVerSection:
        return RichVerSection(
            _version=RichChkEnumTranscoder.decode_enum(
                decoded_chk_section.version, VerVersion
            )
        )

    def encode(
        self,
        rich_chk_section: RichVerSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedVerSection:
        return DecodedVerSection(
            _version=RichChkEnumTranscoder.encode_enum(rich_chk_section.version)
        )
