"""Decode and encode the PUNI - Player Unit Restrictions section."""

import weakref
from typing import Any, cast

from ....model.chk.puni.decoded_puni_section import DecodedPuniSection
from ....model.richchk.puni.rich_puni_section import RichPuniSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)

_NUM_PLAYERS = 12
_NUM_UNITS = 228

_puni_encode_cache: dict[
    Any, Any
] = {}  # id(rich_puni_section) → (weakref(section), DecodedPuniSection)


def _to_2d_bool(flat: list[int], num_rows: int, num_cols: int) -> list[list[bool]]:
    return [
        [bool(flat[r * num_cols + c]) for c in range(num_cols)] for r in range(num_rows)
    ]


def _flatten_bool(matrix: list[list[bool]]) -> list[int]:
    return [int(val) for row in matrix for val in row]


class RichPuniTranscoder(
    RichChkSectionTranscoder[RichPuniSection, DecodedPuniSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedPuniSection.section_name(),
):
    def decode(
        self,
        decoded_chk_section: DecodedPuniSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichPuniSection:
        return RichPuniSection(
            _player_unit_availability=_to_2d_bool(
                decoded_chk_section.player_unit_availability, _NUM_PLAYERS, _NUM_UNITS
            ),
            _global_unit_availability=[
                bool(v) for v in decoded_chk_section.global_unit_availability
            ],
            _player_uses_defaults=_to_2d_bool(
                decoded_chk_section.player_uses_defaults, _NUM_PLAYERS, _NUM_UNITS
            ),
        )

    def encode(
        self,
        rich_chk_section: RichPuniSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedPuniSection:
        cache_key = id(rich_chk_section)
        cached = _puni_encode_cache.get(cache_key)
        if cached is not None and cached[0]() is rich_chk_section:
            return cast(DecodedPuniSection, cached[1])
        result = DecodedPuniSection(
            _player_unit_availability=_flatten_bool(
                rich_chk_section.player_unit_availability
            ),
            _global_unit_availability=[
                int(v) for v in rich_chk_section.global_unit_availability
            ],
            _player_uses_defaults=_flatten_bool(rich_chk_section.player_uses_defaults),
        )
        _puni_encode_cache[cache_key] = (
            weakref.ref(
                rich_chk_section, lambda _: _puni_encode_cache.pop(cache_key, None)
            ),
            result,
        )
        return result
