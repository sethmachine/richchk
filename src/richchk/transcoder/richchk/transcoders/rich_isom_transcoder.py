"""Decode and encode ISOM - Isometric Terrain.

Simple pass-through: the rich representation is identical to the decoded one.
"""

import weakref
from typing import Any, cast

from ....model.chk.isom.decoded_isom_section import DecodedIsomSection
from ....model.richchk.isom.rich_isom_section import RichIsomSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)

_isom_encode_cache: dict[
    Any, Any
] = {}  # id(rich_isom_section) -> (weakref(section), DecodedIsomSection)


class RichIsomTranscoder(
    RichChkSectionTranscoder[RichIsomSection, DecodedIsomSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedIsomSection.section_name(),
):
    def decode(
        self,
        decoded_chk_section: DecodedIsomSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichIsomSection:
        return RichIsomSection(_data=decoded_chk_section.data)

    def encode(
        self,
        rich_chk_section: RichIsomSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedIsomSection:
        cache_key = id(rich_chk_section)
        cached = _isom_encode_cache.get(cache_key)
        if cached is not None and cached[0]() is rich_chk_section:
            return cast(DecodedIsomSection, cached[1])
        result = DecodedIsomSection(_data=rich_chk_section.data)
        _isom_encode_cache[cache_key] = (
            weakref.ref(
                rich_chk_section, lambda _: _isom_encode_cache.pop(cache_key, None)
            ),
            result,
        )
        return result
