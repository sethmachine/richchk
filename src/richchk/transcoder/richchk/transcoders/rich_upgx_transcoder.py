"""Decode and encode the UPGx - Brood War Upgrade Settings section."""

import weakref
from typing import Any, cast

from ....model.chk.upgx.decoded_upgx_section import DecodedUpgxSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....model.richchk.upgrades.upgrade_id import UpgradeId
from ....model.richchk.upgs.upgrade_cost_setting import UpgradeCostSetting
from ....model.richchk.upgx.rich_upgx_section import RichUpgxSection
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)

_ALL_UPGRADES = list(UpgradeId)

_upgx_encode_cache: dict[
    Any, Any
] = {}  # id(rich_upgx_section) → (weakref(section), DecodedUpgxSection)


class RichUpgxTranscoder(
    RichChkSectionTranscoder[RichUpgxSection, DecodedUpgxSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedUpgxSection.section_name(),
):
    def decode(
        self,
        decoded_chk_section: DecodedUpgxSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichUpgxSection:
        settings = {
            upgrade: UpgradeCostSetting(
                _upgrade_id=upgrade,
                _uses_default_settings=bool(
                    decoded_chk_section.uses_default_settings[upgrade.id]
                ),
                _base_mineral_cost=decoded_chk_section.base_mineral_cost[upgrade.id],
                _mineral_cost_factor=decoded_chk_section.mineral_cost_factor[
                    upgrade.id
                ],
                _base_gas_cost=decoded_chk_section.base_gas_cost[upgrade.id],
                _gas_cost_factor=decoded_chk_section.gas_cost_factor[upgrade.id],
                _base_research_time=decoded_chk_section.base_research_time[upgrade.id],
                _research_time_factor=decoded_chk_section.research_time_factor[
                    upgrade.id
                ],
            )
            for upgrade in _ALL_UPGRADES
        }
        return RichUpgxSection(_upgrade_cost_settings=settings)

    def encode(
        self,
        rich_chk_section: RichUpgxSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedUpgxSection:
        cache_key = id(rich_chk_section)
        cached = _upgx_encode_cache.get(cache_key)
        if cached is not None and cached[0]() is rich_chk_section:
            return cast(DecodedUpgxSection, cached[1])
        settings = [rich_chk_section.upgrade_cost_settings[u] for u in _ALL_UPGRADES]
        result = DecodedUpgxSection(
            _uses_default_settings=[int(s.uses_default_settings) for s in settings],
            _base_mineral_cost=[s.base_mineral_cost for s in settings],
            _mineral_cost_factor=[s.mineral_cost_factor for s in settings],
            _base_gas_cost=[s.base_gas_cost for s in settings],
            _gas_cost_factor=[s.gas_cost_factor for s in settings],
            _base_research_time=[s.base_research_time for s in settings],
            _research_time_factor=[s.research_time_factor for s in settings],
        )
        _upgx_encode_cache[cache_key] = (
            weakref.ref(
                rich_chk_section, lambda _: _upgx_encode_cache.pop(cache_key, None)
            ),
            result,
        )
        return result
