"""Decode TILE."""
import weakref
from typing import Any, cast

from ....model.chk.tile.decoded_tile_section import DecodedTileSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....model.richchk.tile.rich_tile_section import RichTileSection
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)
from ....util import logger

_tile_encode_cache: dict[
    Any, Any
] = {}  # id(rich_tile_section) -> (weakref(section), DecodedTileSection)


class RichTileTranscoder(
    RichChkSectionTranscoder[RichTileSection, DecodedTileSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedTileSection.section_name(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(RichTileTranscoder.__name__)

    def decode(
        self,
        decoded_chk_section: DecodedTileSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichTileSection:
        return RichTileSection(
            _tiles=decoded_chk_section.tiles,
        )

    def encode(
        self,
        rich_chk_section: RichTileSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTileSection:
        cache_key = id(rich_chk_section)
        cached = _tile_encode_cache.get(cache_key)
        if cached is not None and cached[0]() is rich_chk_section:
            return cast(DecodedTileSection, cached[1])
        result = DecodedTileSection(
            _tiles=rich_chk_section.tiles,
        )
        _tile_encode_cache[cache_key] = (
            weakref.ref(
                rich_chk_section, lambda _: _tile_encode_cache.pop(cache_key, None)
            ),
            result,
        )
        return result
