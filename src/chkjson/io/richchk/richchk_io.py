import logging
from typing import Any, Union

from ...model.chk.decoded_chk import DecodedChk
from ...model.chk.decoded_chk_section import DecodedChkSection
from ...model.chk.str.decoded_str_section import DecodedStrSection
from ...model.chk.unknown.decoded_unknown_section import DecodedUnknownSection
from ...model.chk_section_name import ChkSectionName
from ...model.richchk.rich_chk import RichChk
from ...model.richchk.rich_chk_section import RichChkSection
from ...model.richchk.richchk_decode_context import RichChkDecodeContext
from ...model.richchk.str.rich_str_lookup import RichStrLookup
from ...transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ...transcoder.richchk.richchk_section_transcoder_factory import (
    RichChkSectionTranscoderFactory,
)
from ...util import logger
from .rich_str_lookup_builder import RichStrLookupBuilder


class RichChkIo:
    def __init__(self) -> None:
        self.log: logging.Logger = logger.get_logger(RichChkIo.__name__)

    def decode_chk(self, chk: DecodedChk) -> RichChk:
        decode_context = self._build_decode_context(chk)
        sections: list[Union[RichChkSection, DecodedChkSection]] = []
        for decoded_chk_section in chk.decoded_chk_sections:
            if isinstance(decoded_chk_section, DecodedUnknownSection):
                sections.append(decoded_chk_section)
            if not RichChkSectionTranscoderFactory.supports_transcoding_chk_section(
                decoded_chk_section.section_name()
            ):
                sections.append(decoded_chk_section)
            else:
                transcoder: RichChkSectionTranscoder[
                    Any, Any
                ] = RichChkSectionTranscoderFactory.make_chk_section_transcoder(
                    decoded_chk_section.section_name()
                )
                sections.append(transcoder.decode(decoded_chk_section, decode_context))
        return RichChk(_chk_sections=sections)

    def _build_decode_context(self, chk: DecodedChk) -> RichChkDecodeContext:
        return RichChkDecodeContext(_rich_str_lookup=self._build_rich_str_lookup(chk))

    def _build_rich_str_lookup(self, chk: DecodedChk) -> RichStrLookup:
        str_sections = chk.get_sections_by_name(ChkSectionName.STR)
        if not str_sections:
            msg = (
                "The decoded CHK has no STR section present! "
                "The CHK is not valid.  Only pass in valid CHK data."
            )
            self.log.error(msg)
            raise ValueError(msg)
        if len(str_sections) > 1:
            msg = (
                "The decoded CHK has more than 1 STR section present! "
                "The CHK may be valid but this case is not handled. "
                "Only pass in CHK data with a single STR section."
            )
            self.log.error(msg)
            raise ValueError(msg)
        only_str: DecodedStrSection = DecodedChkSection.cast(
            str_sections[0], DecodedStrSection
        )
        return RichStrLookupBuilder().build_lookup(only_str)

    def encode_chk(self, rich_chk: RichChk) -> DecodedChk:
        return DecodedChk([])
