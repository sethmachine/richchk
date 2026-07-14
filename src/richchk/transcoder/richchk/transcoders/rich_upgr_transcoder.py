"""Decode and encode the UPGR - Classic Upgrade Restrictions section."""

import weakref
from typing import Any, cast

from ....model.chk.upgr.decoded_upgr_section import DecodedUpgrSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....model.richchk.trig.player_id import PlayerId
from ....model.richchk.upgr.rich_upgr_section import RichUpgrSection
from ....model.richchk.upgrades.upgrade_id import UpgradeId
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)

_GAME_PLAYERS = [p for p in PlayerId if p.id < 12]
_CLASSIC_UPGRADES = [u for u in UpgradeId if u.id < 46]

_NUM_UPGRADES = 46

_upgr_encode_cache: dict[
    Any, Any
] = {}  # id(rich_upgr_section) → (weakref(section), DecodedUpgrSection)


class RichUpgrTranscoder(
    RichChkSectionTranscoder[RichUpgrSection, DecodedUpgrSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedUpgrSection.section_name(),
):
    def decode(
        self,
        decoded_chk_section: DecodedUpgrSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichUpgrSection:
        player_max = {
            player: {
                upgrade: decoded_chk_section.player_max_levels[
                    player.id * _NUM_UPGRADES + upgrade.id
                ]
                for upgrade in _CLASSIC_UPGRADES
            }
            for player in _GAME_PLAYERS
        }
        player_start = {
            player: {
                upgrade: decoded_chk_section.player_start_levels[
                    player.id * _NUM_UPGRADES + upgrade.id
                ]
                for upgrade in _CLASSIC_UPGRADES
            }
            for player in _GAME_PLAYERS
        }
        global_max = {
            upgrade: decoded_chk_section.global_max_levels[upgrade.id]
            for upgrade in _CLASSIC_UPGRADES
        }
        global_start = {
            upgrade: decoded_chk_section.global_start_levels[upgrade.id]
            for upgrade in _CLASSIC_UPGRADES
        }
        player_defaults = {
            player: {
                upgrade: bool(
                    decoded_chk_section.player_uses_defaults[
                        player.id * _NUM_UPGRADES + upgrade.id
                    ]
                )
                for upgrade in _CLASSIC_UPGRADES
            }
            for player in _GAME_PLAYERS
        }
        return RichUpgrSection(
            _player_max_levels=player_max,
            _player_start_levels=player_start,
            _global_max_levels=global_max,
            _global_start_levels=global_start,
            _player_uses_defaults=player_defaults,
        )

    def encode(
        self,
        rich_chk_section: RichUpgrSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedUpgrSection:
        cache_key = id(rich_chk_section)
        cached = _upgr_encode_cache.get(cache_key)
        if cached is not None and cached[0]() is rich_chk_section:
            return cast(DecodedUpgrSection, cached[1])
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
        result = DecodedUpgrSection(
            _player_max_levels=flat_max,
            _player_start_levels=flat_start,
            _global_max_levels=global_max,
            _global_start_levels=global_start,
            _player_uses_defaults=flat_defaults,
        )
        _upgr_encode_cache[cache_key] = (
            weakref.ref(
                rich_chk_section, lambda _: _upgr_encode_cache.pop(cache_key, None)
            ),
            result,
        )
        return result
