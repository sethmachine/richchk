"""Decode and encode the PUNI - Player Unit Restrictions section."""

import weakref
from typing import Any, cast

from ....model.chk.puni.decoded_puni_section import DecodedPuniSection
from ....model.richchk.puni.rich_puni_section import RichPuniSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....model.richchk.trig.player_id import PlayerId
from ....model.richchk.unis.unit_id import UnitId
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)

_GAME_PLAYERS = [p for p in PlayerId if p.id < 12]
_GAME_UNITS = [u for u in UnitId if u.id < 228]

_NUM_UNITS = 228

_puni_encode_cache: dict[
    Any, Any
] = {}  # id(rich_puni_section) → (weakref(section), DecodedPuniSection)


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
        player_availability = {
            player: {
                unit: bool(
                    decoded_chk_section.player_unit_availability[
                        player.id * _NUM_UNITS + unit.id
                    ]
                )
                for unit in _GAME_UNITS
            }
            for player in _GAME_PLAYERS
        }
        global_availability = {
            unit: bool(decoded_chk_section.global_unit_availability[unit.id])
            for unit in _GAME_UNITS
        }
        player_defaults = {
            player: {
                unit: bool(
                    decoded_chk_section.player_uses_defaults[
                        player.id * _NUM_UNITS + unit.id
                    ]
                )
                for unit in _GAME_UNITS
            }
            for player in _GAME_PLAYERS
        }
        return RichPuniSection(
            _player_unit_availability=player_availability,
            _global_unit_availability=global_availability,
            _player_uses_defaults=player_defaults,
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
        flat_availability = [0] * (12 * _NUM_UNITS)
        for player, units in rich_chk_section.player_unit_availability.items():
            for unit, avail in units.items():
                flat_availability[player.id * _NUM_UNITS + unit.id] = int(avail)
        global_flat = [0] * _NUM_UNITS
        for unit, avail in rich_chk_section.global_unit_availability.items():
            global_flat[unit.id] = int(avail)
        flat_defaults = [0] * (12 * _NUM_UNITS)
        for player, units in rich_chk_section.player_uses_defaults.items():
            for unit, uses_default in units.items():
                flat_defaults[player.id * _NUM_UNITS + unit.id] = int(uses_default)
        result = DecodedPuniSection(
            _player_unit_availability=flat_availability,
            _global_unit_availability=global_flat,
            _player_uses_defaults=flat_defaults,
        )
        _puni_encode_cache[cache_key] = (
            weakref.ref(
                rich_chk_section, lambda _: _puni_encode_cache.pop(cache_key, None)
            ),
            result,
        )
        return result
