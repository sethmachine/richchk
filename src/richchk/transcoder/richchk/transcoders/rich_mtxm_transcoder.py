"""Decode MTXM."""
import weakref
from typing import Any, cast

from ....model.chk.mtxm.decoded_mtxm_section import DecodedMtxmSection
from ....model.richchk.mtxm.rich_mtxm_section import RichMtxmSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)
from ....util import logger

_mtxm_encode_cache: dict[
    Any, Any
] = {}  # id(rich_mtxm_section) -> (weakref(section), DecodedMtxmSection)


class RichMtxmTranscoder(
    RichChkSectionTranscoder[RichMtxmSection, DecodedMtxmSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedMtxmSection.section_name(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(RichMtxmTranscoder.__name__)

    def decode(
        self,
        decoded_chk_section: DecodedMtxmSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichMtxmSection:
        return RichMtxmSection(
            _tiles=decoded_chk_section.tiles,
        )

    def encode(
        self,
        rich_chk_section: RichMtxmSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedMtxmSection:
        cache_key = id(rich_chk_section)
        cached = _mtxm_encode_cache.get(cache_key)
        if cached is not None and cached[0]() is rich_chk_section:
            return cast(DecodedMtxmSection, cached[1])
        result = DecodedMtxmSection(
            _tiles=rich_chk_section.tiles,
        )
        _mtxm_encode_cache[cache_key] = (
            weakref.ref(
                rich_chk_section, lambda _: _mtxm_encode_cache.pop(cache_key, None)
            ),
            result,
        )
        return result
