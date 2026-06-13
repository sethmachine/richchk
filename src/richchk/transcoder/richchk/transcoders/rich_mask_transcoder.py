"""Decode and encode MASK - Fog of War.

Simple pass-through: the rich representation is identical to the decoded one.
"""

import weakref
from typing import Any, cast

from ....model.chk.mask.decoded_mask_section import DecodedMaskSection
from ....model.richchk.mask.rich_mask_section import RichMaskSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)

_mask_encode_cache: dict[
    Any, Any
] = {}  # id(rich_mask_section) -> (weakref(section), DecodedMaskSection)


class RichMaskTranscoder(
    RichChkSectionTranscoder[RichMaskSection, DecodedMaskSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedMaskSection.section_name(),
):
    def decode(
        self,
        decoded_chk_section: DecodedMaskSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichMaskSection:
        return RichMaskSection(_fog_data=list(decoded_chk_section.fog_data))

    def encode(
        self,
        rich_chk_section: RichMaskSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedMaskSection:
        cache_key = id(rich_chk_section)
        cached = _mask_encode_cache.get(cache_key)
        if cached is not None and cached[0]() is rich_chk_section:
            return cast(DecodedMaskSection, cached[1])
        result = DecodedMaskSection(_fog_data=tuple(rich_chk_section.fog_data))
        _mask_encode_cache[cache_key] = (
            weakref.ref(
                rich_chk_section, lambda _: _mask_encode_cache.pop(cache_key, None)
            ),
            result,
        )
        return result
