"""Decode and encode the OWNR - StarCraft Player Types section."""

import weakref
from typing import Any, cast

from ....model.chk.ownr.decoded_ownr_section import DecodedOwnrSection
from ....model.richchk.ownr.player_type import PlayerType
from ....model.richchk.ownr.rich_ownr_section import RichOwnrSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)
from ....transcoder.richchk.transcoders.helpers.richchk_enum_transcoder import (
    RichChkEnumTranscoder,
)

_ownr_encode_cache: dict[
    Any, Any
] = {}  # id(rich_ownr_section) → (weakref(section), DecodedOwnrSection)


class RichOwnrTranscoder(
    RichChkSectionTranscoder[RichOwnrSection, DecodedOwnrSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedOwnrSection.section_name(),
):
    def decode(
        self,
        decoded_chk_section: DecodedOwnrSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichOwnrSection:
        return RichOwnrSection(
            _player_types=[
                RichChkEnumTranscoder.decode_enum(type_id, PlayerType)
                for type_id in decoded_chk_section.player_controllers
            ]
        )

    def encode(
        self,
        rich_chk_section: RichOwnrSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedOwnrSection:
        cache_key = id(rich_chk_section)
        cached = _ownr_encode_cache.get(cache_key)
        if cached is not None and cached[0]() is rich_chk_section:
            return cast(DecodedOwnrSection, cached[1])
        result = DecodedOwnrSection(
            _player_controllers=[
                RichChkEnumTranscoder.encode_enum(player_type)
                for player_type in rich_chk_section.player_types
            ]
        )
        _ownr_encode_cache[cache_key] = (
            weakref.ref(
                rich_chk_section, lambda _: _ownr_encode_cache.pop(cache_key, None)
            ),
            result,
        )
        return result
