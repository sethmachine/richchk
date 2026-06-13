"""Decode ERA."""
import weakref
from typing import Any, cast

from ....model.chk.era.decoded_era_section import DecodedEraSection
from ....model.richchk.era.rich_era_section import RichEraSection
from ....model.richchk.era.tileset import StarCraftTileset
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)
from ....util import logger
from .helpers.richchk_enum_transcoder import RichChkEnumTranscoder

_era_encode_cache: dict[
    Any, Any
] = {}  # id(rich_era_section) -> (weakref(section), DecodedEraSection)


class RichEraTranscoder(
    RichChkSectionTranscoder[RichEraSection, DecodedEraSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedEraSection.section_name(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(RichEraTranscoder.__name__)

    def decode(
        self,
        decoded_chk_section: DecodedEraSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichEraSection:
        return RichEraSection(
            _tileset=RichChkEnumTranscoder.decode_enum(
                decoded_chk_section.tileset, StarCraftTileset
            )
        )

    def encode(
        self,
        rich_chk_section: RichEraSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedEraSection:
        cache_key = id(rich_chk_section)
        cached = _era_encode_cache.get(cache_key)
        if cached is not None and cached[0]() is rich_chk_section:
            return cast(DecodedEraSection, cached[1])
        result = DecodedEraSection(
            _tileset=RichChkEnumTranscoder.encode_enum(rich_chk_section.tileset)
        )
        _era_encode_cache[cache_key] = (
            weakref.ref(
                rich_chk_section, lambda _: _era_encode_cache.pop(cache_key, None)
            ),
            result,
        )
        return result
