"""Decode and encode the SPRP - Scenario Properties section."""

from ....model.chk.sprp.decoded_sprp_section import DecodedSprpSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....model.richchk.sprp.rich_sprp_section import RichSprpSection
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)
from ....util import logger


class RichSprpTranscoder(
    RichChkSectionTranscoder[RichSprpSection, DecodedSprpSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedSprpSection.section_name(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(RichSprpTranscoder.__name__)

    def decode(
        self,
        decoded_chk_section: DecodedSprpSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichSprpSection:
        return RichSprpSection(
            _scenario_name=rich_chk_decode_context.rich_str_lookup.get_string_by_id(
                decoded_chk_section.scenario_name_string_id
            ),
            _scenario_description=rich_chk_decode_context.rich_str_lookup.get_string_by_id(
                decoded_chk_section.scenario_description_string_id
            ),
        )

    def encode(
        self,
        rich_chk_section: RichSprpSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedSprpSection:
        result = DecodedSprpSection(
            _scenario_name_string_id=rich_chk_encode_context.rich_str_lookup.get_id_by_string(
                rich_chk_section.scenario_name
            ),
            _scenario_description_string_id=rich_chk_encode_context.rich_str_lookup.get_id_by_string(
                rich_chk_section.scenario_description
            ),
        )
        return result
