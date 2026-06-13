"""Decode and encode DD2 - Doodads.

The rich transcoder converts the enabled field between int (0/1) and bool.
"""

import weakref
from typing import Any, cast

from ....model.chk.dd2.decoded_dd2_entry import DecodedDd2Entry
from ....model.chk.dd2.decoded_dd2_section import DecodedDd2Section
from ....model.richchk.dd2.rich_dd2_entry import RichDoodad
from ....model.richchk.dd2.rich_dd2_section import RichDd2Section
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)

_dd2_encode_cache: dict[
    Any, Any
] = {}  # id(rich_dd2_section) -> (weakref(section), DecodedDd2Section)


class RichDd2Transcoder(
    RichChkSectionTranscoder[RichDd2Section, DecodedDd2Section],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedDd2Section.section_name(),
):
    def decode(
        self,
        decoded_chk_section: DecodedDd2Section,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichDd2Section:
        rich_doodads = [
            RichDoodad(
                _doodad_id=entry.doodad_id,
                _x=entry.x,
                _y=entry.y,
                _owner=entry.owner,
                _enabled=bool(entry.enabled),
            )
            for entry in decoded_chk_section.entries
        ]
        return RichDd2Section(_doodads=rich_doodads)

    def encode(
        self,
        rich_chk_section: RichDd2Section,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedDd2Section:
        cache_key = id(rich_chk_section)
        cached = _dd2_encode_cache.get(cache_key)
        if cached is not None and cached[0]() is rich_chk_section:
            return cast(DecodedDd2Section, cached[1])
        decoded_entries = tuple(
            DecodedDd2Entry(
                _doodad_id=doodad.doodad_id,
                _x=doodad.x,
                _y=doodad.y,
                _owner=doodad.owner,
                _enabled=1 if doodad.enabled else 0,
            )
            for doodad in rich_chk_section.doodads
        )
        result = DecodedDd2Section(_entries=decoded_entries)
        _dd2_encode_cache[cache_key] = (
            weakref.ref(
                rich_chk_section, lambda _: _dd2_encode_cache.pop(cache_key, None)
            ),
            result,
        )
        return result
