"""Decode and encode the PTEC - Classic Tech Restrictions section."""

import weakref
from typing import Any, cast

from ....model.chk.ptec.decoded_ptec_section import DecodedPtecSection
from ....model.richchk.ptec.rich_ptec_section import RichPtecSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)

_NUM_PLAYERS = 12
_NUM_TECHS = 24

_ptec_encode_cache: dict[
    Any, Any
] = {}  # id(rich_ptec_section) → (weakref(section), DecodedPtecSection)


def _to_2d_bool(flat: list[int], num_rows: int, num_cols: int) -> list[list[bool]]:
    return [
        [bool(flat[r * num_cols + c]) for c in range(num_cols)] for r in range(num_rows)
    ]


def _flatten_bool(matrix: list[list[bool]]) -> list[int]:
    return [int(val) for row in matrix for val in row]


class RichPtecTranscoder(
    RichChkSectionTranscoder[RichPtecSection, DecodedPtecSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedPtecSection.section_name(),
):
    def decode(
        self,
        decoded_chk_section: DecodedPtecSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichPtecSection:
        return RichPtecSection(
            _player_tech_availability=_to_2d_bool(
                decoded_chk_section.player_tech_availability, _NUM_PLAYERS, _NUM_TECHS
            ),
            _player_tech_researched=_to_2d_bool(
                decoded_chk_section.player_tech_researched, _NUM_PLAYERS, _NUM_TECHS
            ),
            _global_tech_availability=[
                bool(v) for v in decoded_chk_section.global_tech_availability
            ],
            _global_tech_researched=[
                bool(v) for v in decoded_chk_section.global_tech_researched
            ],
            _player_uses_defaults=_to_2d_bool(
                decoded_chk_section.player_uses_defaults, _NUM_PLAYERS, _NUM_TECHS
            ),
        )

    def encode(
        self,
        rich_chk_section: RichPtecSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedPtecSection:
        cache_key = id(rich_chk_section)
        cached = _ptec_encode_cache.get(cache_key)
        if cached is not None and cached[0]() is rich_chk_section:
            return cast(DecodedPtecSection, cached[1])
        result = DecodedPtecSection(
            _player_tech_availability=_flatten_bool(
                rich_chk_section.player_tech_availability
            ),
            _player_tech_researched=_flatten_bool(
                rich_chk_section.player_tech_researched
            ),
            _global_tech_availability=[
                int(v) for v in rich_chk_section.global_tech_availability
            ],
            _global_tech_researched=[
                int(v) for v in rich_chk_section.global_tech_researched
            ],
            _player_uses_defaults=_flatten_bool(rich_chk_section.player_uses_defaults),
        )
        _ptec_encode_cache[cache_key] = (
            weakref.ref(
                rich_chk_section, lambda _: _ptec_encode_cache.pop(cache_key, None)
            ),
            result,
        )
        return result
