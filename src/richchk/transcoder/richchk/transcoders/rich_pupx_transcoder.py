"""Decode and encode the PUPx - Brood War Upgrade Restrictions section."""

import weakref
from typing import Any, cast

from ....model.chk.pupx.decoded_pupx_section import DecodedPupxSection
from ....model.richchk.pupx.rich_pupx_section import RichPupxSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)

_NUM_PLAYERS = 12
_NUM_UPGRADES = 61

_pupx_encode_cache: dict[
    Any, Any
] = {}  # id(rich_pupx_section) → (weakref(section), DecodedPupxSection)


def _to_2d_int(flat: list[int], num_rows: int, num_cols: int) -> list[list[int]]:
    return [[flat[r * num_cols + c] for c in range(num_cols)] for r in range(num_rows)]


def _to_2d_bool(flat: list[int], num_rows: int, num_cols: int) -> list[list[bool]]:
    return [
        [bool(flat[r * num_cols + c]) for c in range(num_cols)] for r in range(num_rows)
    ]


def _flatten_int(matrix: list[list[int]]) -> list[int]:
    return [val for row in matrix for val in row]


def _flatten_bool(matrix: list[list[bool]]) -> list[int]:
    return [int(val) for row in matrix for val in row]


class RichPupxTranscoder(
    RichChkSectionTranscoder[RichPupxSection, DecodedPupxSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedPupxSection.section_name(),
):
    def decode(
        self,
        decoded_chk_section: DecodedPupxSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichPupxSection:
        return RichPupxSection(
            _player_max_levels=_to_2d_int(
                decoded_chk_section.player_max_levels, _NUM_PLAYERS, _NUM_UPGRADES
            ),
            _player_start_levels=_to_2d_int(
                decoded_chk_section.player_start_levels, _NUM_PLAYERS, _NUM_UPGRADES
            ),
            _global_max_levels=list(decoded_chk_section.global_max_levels),
            _global_start_levels=list(decoded_chk_section.global_start_levels),
            _player_uses_defaults=_to_2d_bool(
                decoded_chk_section.player_uses_defaults, _NUM_PLAYERS, _NUM_UPGRADES
            ),
        )

    def encode(
        self,
        rich_chk_section: RichPupxSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedPupxSection:
        cache_key = id(rich_chk_section)
        cached = _pupx_encode_cache.get(cache_key)
        if cached is not None and cached[0]() is rich_chk_section:
            return cast(DecodedPupxSection, cached[1])
        result = DecodedPupxSection(
            _player_max_levels=_flatten_int(rich_chk_section.player_max_levels),
            _player_start_levels=_flatten_int(rich_chk_section.player_start_levels),
            _global_max_levels=list(rich_chk_section.global_max_levels),
            _global_start_levels=list(rich_chk_section.global_start_levels),
            _player_uses_defaults=_flatten_bool(rich_chk_section.player_uses_defaults),
        )
        _pupx_encode_cache[cache_key] = (
            weakref.ref(
                rich_chk_section, lambda _: _pupx_encode_cache.pop(cache_key, None)
            ),
            result,
        )
        return result
