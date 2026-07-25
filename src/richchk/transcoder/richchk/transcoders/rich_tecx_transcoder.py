"""Decode and encode the TECx - Brood War Tech Settings section."""

import weakref
from typing import Any, cast

from ....model.chk.tecx.decoded_tecx_section import DecodedTecxSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....model.richchk.techs.tech_id import TechId
from ....model.richchk.tecs.tech_cost_setting import TechCostSetting
from ....model.richchk.tecx.rich_tecx_section import RichTecxSection
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)

_ALL_TECHS = list(TechId)

_tecx_encode_cache: dict[
    Any, Any
] = {}  # id(rich_tecx_section) → (weakref(section), DecodedTecxSection)


class RichTecxTranscoder(
    RichChkSectionTranscoder[RichTecxSection, DecodedTecxSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedTecxSection.section_name(),
):
    def decode(
        self,
        decoded_chk_section: DecodedTecxSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichTecxSection:
        settings = {
            tech: TechCostSetting(
                _tech_id=tech,
                _uses_default_settings=bool(
                    decoded_chk_section.uses_default_settings[tech.id]
                ),
                _mineral_cost=decoded_chk_section.mineral_cost[tech.id],
                _gas_cost=decoded_chk_section.gas_cost[tech.id],
                _research_time=decoded_chk_section.research_time[tech.id],
                _energy_cost=decoded_chk_section.energy_cost[tech.id],
            )
            for tech in _ALL_TECHS
        }
        return RichTecxSection(_tech_cost_settings=settings)

    def encode(
        self,
        rich_chk_section: RichTecxSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTecxSection:
        cache_key = id(rich_chk_section)
        cached = _tecx_encode_cache.get(cache_key)
        if cached is not None and cached[0]() is rich_chk_section:
            return cast(DecodedTecxSection, cached[1])
        settings = [rich_chk_section.tech_cost_settings[t] for t in _ALL_TECHS]
        result = DecodedTecxSection(
            _uses_default_settings=[int(s.uses_default_settings) for s in settings],
            _mineral_cost=[s.mineral_cost for s in settings],
            _gas_cost=[s.gas_cost for s in settings],
            _research_time=[s.research_time for s in settings],
            _energy_cost=[s.energy_cost for s in settings],
        )
        _tecx_encode_cache[cache_key] = (
            weakref.ref(
                rich_chk_section, lambda _: _tecx_encode_cache.pop(cache_key, None)
            ),
            result,
        )
        return result
