"""Decode and encode the TECS - Classic Tech Settings section."""


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

_CLASSIC_TECHS = [t for t in TechId if t.id < 24]


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
            for tech in _CLASSIC_TECHS
        }
        return RichTecsSection(_tech_cost_settings=settings)

    def encode(
        self,
        rich_chk_section: RichTecsSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTecsSection:
        settings = [rich_chk_section.tech_cost_settings[t] for t in _CLASSIC_TECHS]
        result = DecodedTecsSection(
            _uses_default_settings=[int(s.uses_default_settings) for s in settings],
            _mineral_cost=[s.mineral_cost for s in settings],
            _gas_cost=[s.gas_cost for s in settings],
            _research_time=[s.research_time for s in settings],
            _energy_cost=[s.energy_cost for s in settings],
        )
        return result
