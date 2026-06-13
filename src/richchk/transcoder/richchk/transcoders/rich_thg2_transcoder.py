"""Decode and encode THG2 - Sprites.

The rich transcoder drops the unused padding byte on decode and hardcodes it to 0 on
encode.
"""

import weakref
from typing import Any, cast

from ....model.chk.thg2.decoded_thg2_entry import DecodedThg2Entry
from ....model.chk.thg2.decoded_thg2_section import DecodedThg2Section
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....model.richchk.thg2.rich_thg2_entry import RichThg2Entry
from ....model.richchk.thg2.rich_thg2_section import RichThg2Section
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)

_thg2_encode_cache: dict[
    Any, Any
] = {}  # id(rich_thg2_section) -> (weakref(section), DecodedThg2Section)


class RichThg2Transcoder(
    RichChkSectionTranscoder[RichThg2Section, DecodedThg2Section],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedThg2Section.section_name(),
):
    def decode(
        self,
        decoded_chk_section: DecodedThg2Section,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichThg2Section:
        rich_entries = tuple(
            RichThg2Entry(
                _sprite_id=entry.sprite_id,
                _x=entry.x,
                _y=entry.y,
                _owner=entry.owner,
                _flags=entry.flags,
            )
            for entry in decoded_chk_section.entries
        )
        return RichThg2Section(_entries=rich_entries)

    def encode(
        self,
        rich_chk_section: RichThg2Section,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedThg2Section:
        cache_key = id(rich_chk_section)
        cached = _thg2_encode_cache.get(cache_key)
        if cached is not None and cached[0]() is rich_chk_section:
            return cast(DecodedThg2Section, cached[1])
        decoded_entries = tuple(
            DecodedThg2Entry(
                _sprite_id=entry.sprite_id,
                _x=entry.x,
                _y=entry.y,
                _owner=entry.owner,
                _unused=0,
                _flags=entry.flags,
            )
            for entry in rich_chk_section.entries
        )
        result = DecodedThg2Section(_entries=decoded_entries)
        _thg2_encode_cache[cache_key] = (
            weakref.ref(
                rich_chk_section, lambda _: _thg2_encode_cache.pop(cache_key, None)
            ),
            result,
        )
        return result
