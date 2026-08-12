"""Decode and encode the SPRP - Scenario Properties section."""
import weakref
from typing import Any, cast

from ....model.chk.sprp.decoded_sprp_section import DecodedSprpSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....model.richchk.sprp.rich_sprp_section import RichSprpSection
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)
from ....util import logger

_sprp_encode_cache: dict[
    Any, Any
] = (
    {}
)  # (id(rich_sprp_section), id(str_lookup)) → (weakref(section), DecodedSprpSection)


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
        cache_key = (id(rich_chk_section), id(rich_chk_encode_context.rich_str_lookup))
        cached = _sprp_encode_cache.get(cache_key)
        if cached is not None and cached[0]() is rich_chk_section:
            return cast(DecodedSprpSection, cached[1])
        result = DecodedSprpSection(
            _scenario_name_string_id=rich_chk_encode_context.rich_str_lookup.get_id_by_string(
                rich_chk_section.scenario_name
            ),
            _scenario_description_string_id=rich_chk_encode_context.rich_str_lookup.get_id_by_string(
                rich_chk_section.scenario_description
            ),
        )
        _sprp_encode_cache[cache_key] = (
            weakref.ref(
                rich_chk_section, lambda _: _sprp_encode_cache.pop(cache_key, None)
            ),
            result,
        )
        return result
