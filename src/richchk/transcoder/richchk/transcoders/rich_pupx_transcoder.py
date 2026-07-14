"""Decode and encode the PUPx - Brood War Upgrade Restrictions section."""

import weakref
from typing import Any, cast

from ....model.chk.pupx.decoded_pupx_section import DecodedPupxSection
from ....model.richchk.pupx.rich_pupx_section import RichPupxSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....model.richchk.trig.player_id import PlayerId
from ....model.richchk.upgrades.upgrade_id import UpgradeId
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)

_GAME_PLAYERS = [p for p in PlayerId if p.id < 12]
_BW_UPGRADES = list(UpgradeId)

_NUM_UPGRADES = 61

_pupx_encode_cache: dict[
    Any, Any
] = {}  # id(rich_pupx_section) → (weakref(section), DecodedPupxSection)


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
        player_max = {
            player: {
                upgrade: decoded_chk_section.player_max_levels[
                    player.id * _NUM_UPGRADES + upgrade.id
                ]
                for upgrade in _BW_UPGRADES
            }
            for player in _GAME_PLAYERS
        }
        player_start = {
            player: {
                upgrade: decoded_chk_section.player_start_levels[
                    player.id * _NUM_UPGRADES + upgrade.id
                ]
                for upgrade in _BW_UPGRADES
            }
            for player in _GAME_PLAYERS
        }
        global_max = {
            upgrade: decoded_chk_section.global_max_levels[upgrade.id]
            for upgrade in _BW_UPGRADES
        }
        global_start = {
            upgrade: decoded_chk_section.global_start_levels[upgrade.id]
            for upgrade in _BW_UPGRADES
        }
        player_defaults = {
            player: {
                upgrade: bool(
                    decoded_chk_section.player_uses_defaults[
                        player.id * _NUM_UPGRADES + upgrade.id
                    ]
                )
                for upgrade in _BW_UPGRADES
            }
            for player in _GAME_PLAYERS
        }
        return RichPupxSection(
            _player_max_levels=player_max,
            _player_start_levels=player_start,
            _global_max_levels=global_max,
            _global_start_levels=global_start,
            _player_uses_defaults=player_defaults,
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
        flat_max = [0] * (12 * _NUM_UPGRADES)
        for player, upgrades in rich_chk_section.player_max_levels.items():
            for upgrade, level in upgrades.items():
                flat_max[player.id * _NUM_UPGRADES + upgrade.id] = level
        flat_start = [0] * (12 * _NUM_UPGRADES)
        for player, upgrades in rich_chk_section.player_start_levels.items():
            for upgrade, level in upgrades.items():
                flat_start[player.id * _NUM_UPGRADES + upgrade.id] = level
        global_max = [0] * _NUM_UPGRADES
        for upgrade, level in rich_chk_section.global_max_levels.items():
            global_max[upgrade.id] = level
        global_start = [0] * _NUM_UPGRADES
        for upgrade, level in rich_chk_section.global_start_levels.items():
            global_start[upgrade.id] = level
        flat_defaults = [0] * (12 * _NUM_UPGRADES)
        for player, player_defaults in rich_chk_section.player_uses_defaults.items():
            for upgrade, uses_default in player_defaults.items():
                flat_defaults[player.id * _NUM_UPGRADES + upgrade.id] = int(
                    uses_default
                )
        result = DecodedPupxSection(
            _player_max_levels=flat_max,
            _player_start_levels=flat_start,
            _global_max_levels=global_max,
            _global_start_levels=global_start,
            _player_uses_defaults=flat_defaults,
        )
        _pupx_encode_cache[cache_key] = (
            weakref.ref(
                rich_chk_section, lambda _: _pupx_encode_cache.pop(cache_key, None)
            ),
            result,
        )
        return result
