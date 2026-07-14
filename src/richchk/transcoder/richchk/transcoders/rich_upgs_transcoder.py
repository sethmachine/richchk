"""Decode and encode the UPGS - Classic Upgrade Settings section."""

import weakref
from typing import Any, cast

from ....model.chk.upgs.decoded_upgs_section import DecodedUpgsSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....model.richchk.upgrades.upgrade_id import UpgradeId
from ....model.richchk.upgs.rich_upgs_section import RichUpgsSection
from ....model.richchk.upgs.upgrade_cost_setting import UpgradeCostSetting
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)
from ....transcoder.richchk.transcoders.helpers.richchk_enum_transcoder import (
    RichChkEnumTranscoder,
)

_NUM_UPGRADES = 46

_upgs_encode_cache: dict[
    Any, Any
] = {}  # id(rich_upgs_section) → (weakref(section), DecodedUpgsSection)


class RichUpgsTranscoder(
    RichChkSectionTranscoder[RichUpgsSection, DecodedUpgsSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedUpgsSection.section_name(),
):
    def decode(
        self,
        decoded_chk_section: DecodedUpgsSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichUpgsSection:
        settings = []
        for i in range(_NUM_UPGRADES):
            upgrade_id = RichChkEnumTranscoder.decode_enum(i, UpgradeId)
            settings.append(
                UpgradeCostSetting(
                    _upgrade_id=upgrade_id,
                    _uses_default_settings=bool(
                        decoded_chk_section.uses_default_settings[i]
                    ),
                    _base_mineral_cost=decoded_chk_section.base_mineral_cost[i],
                    _mineral_cost_factor=decoded_chk_section.mineral_cost_factor[i],
                    _base_gas_cost=decoded_chk_section.base_gas_cost[i],
                    _gas_cost_factor=decoded_chk_section.gas_cost_factor[i],
                    _base_research_time=decoded_chk_section.base_research_time[i],
                    _research_time_factor=decoded_chk_section.research_time_factor[i],
                )
            )
        return RichUpgsSection(_upgrade_cost_settings=settings)

    def encode(
        self,
        rich_chk_section: RichUpgsSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedUpgsSection:
        cache_key = id(rich_chk_section)
        cached = _upgs_encode_cache.get(cache_key)
        if cached is not None and cached[0]() is rich_chk_section:
            return cast(DecodedUpgsSection, cached[1])
        settings = rich_chk_section.upgrade_cost_settings
        result = DecodedUpgsSection(
            _uses_default_settings=[int(s.uses_default_settings) for s in settings],
            _base_mineral_cost=[s.base_mineral_cost for s in settings],
            _mineral_cost_factor=[s.mineral_cost_factor for s in settings],
            _base_gas_cost=[s.base_gas_cost for s in settings],
            _gas_cost_factor=[s.gas_cost_factor for s in settings],
            _base_research_time=[s.base_research_time for s in settings],
            _research_time_factor=[s.research_time_factor for s in settings],
        )
        _upgs_encode_cache[cache_key] = (
            weakref.ref(
                rich_chk_section, lambda _: _upgs_encode_cache.pop(cache_key, None)
            ),
            result,
        )
        return result
