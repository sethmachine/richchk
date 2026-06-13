"""Decode DIM."""
import weakref
from typing import Any, cast

from ....model.chk.dim.decoded_dim_section import DecodedDimSection
from ....model.richchk.dim.rich_dim_section import RichDimSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)
from ....util import logger

_dim_encode_cache: dict[
    Any, Any
] = {}  # id(rich_dim_section) -> (weakref(section), DecodedDimSection)


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
        cache_key = id(rich_chk_section)
        cached = _dim_encode_cache.get(cache_key)
        if cached is not None and cached[0]() is rich_chk_section:
            return cast(DecodedDimSection, cached[1])
        result = DecodedDimSection(
            _width=rich_chk_section.width,
            _height=rich_chk_section.height,
        )
        _dim_encode_cache[cache_key] = (
            weakref.ref(
                rich_chk_section, lambda _: _dim_encode_cache.pop(cache_key, None)
            ),
            result,
        )
        return result
