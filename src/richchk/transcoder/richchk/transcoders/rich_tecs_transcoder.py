"""Decode and encode the TECS - Classic Tech Settings section."""

import weakref
from typing import Any, cast

from ....model.chk.tecs.decoded_tecs_section import DecodedTecsSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....model.richchk.techs.tech_id import TechId
from ....model.richchk.tecs.rich_tecs_section import RichTecsSection
from ....model.richchk.tecs.tech_cost_setting import TechCostSetting
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)
from ....transcoder.richchk.transcoders.helpers.richchk_enum_transcoder import (
    RichChkEnumTranscoder,
)

_NUM_TECHS = 24

_tecs_encode_cache: dict[
    Any, Any
] = {}  # id(rich_tecs_section) → (weakref(section), DecodedTecsSection)


class RichTecsTranscoder(
    RichChkSectionTranscoder[RichTecsSection, DecodedTecsSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedTecsSection.section_name(),
):
    def decode(
        self,
        decoded_chk_section: DecodedTecsSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichTecsSection:
        settings = []
        for i in range(_NUM_TECHS):
            tech_id = RichChkEnumTranscoder.decode_enum(i, TechId)
            settings.append(
                TechCostSetting(
                    _tech_id=tech_id,
                    _uses_default_settings=bool(
                        decoded_chk_section.uses_default_settings[i]
                    ),
                    _mineral_cost=decoded_chk_section.mineral_cost[i],
                    _gas_cost=decoded_chk_section.gas_cost[i],
                    _research_time=decoded_chk_section.research_time[i],
                    _energy_cost=decoded_chk_section.energy_cost[i],
                )
            )
        return RichTecsSection(_tech_cost_settings=settings)

    def encode(
        self,
        rich_chk_section: RichTecsSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTecsSection:
        cache_key = id(rich_chk_section)
        cached = _tecs_encode_cache.get(cache_key)
        if cached is not None and cached[0]() is rich_chk_section:
            return cast(DecodedTecsSection, cached[1])
        settings = rich_chk_section.tech_cost_settings
        result = DecodedTecsSection(
            _uses_default_settings=[int(s.uses_default_settings) for s in settings],
            _mineral_cost=[s.mineral_cost for s in settings],
            _gas_cost=[s.gas_cost for s in settings],
            _research_time=[s.research_time for s in settings],
            _energy_cost=[s.energy_cost for s in settings],
        )
        _tecs_encode_cache[cache_key] = (
            weakref.ref(
                rich_chk_section, lambda _: _tecs_encode_cache.pop(cache_key, None)
            ),
            result,
        )
        return result
