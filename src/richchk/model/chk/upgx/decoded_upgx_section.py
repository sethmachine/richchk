"""UPGx - Brood War Upgrade Settings (global cost overrides).

u8[61]  uses_default_settings:  0=uses custom, 1=uses SC game defaults u16[61]
base_mineral_cost:      base mineral cost per upgrade u16[61] mineral_cost_factor:
mineral cost factor per upgrade u16[61] base_gas_cost:          base gas cost per
upgrade u16[61] gas_cost_factor:        gas cost factor per upgrade u16[61]
base_research_time:     base research time per upgrade u16[61] research_time_factor:
research time factor per upgrade

Total: 61 + 6*(2*61) = 61 + 732 = 793 bytes.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..decoded_chk_section import DecodedChkSection

_NUM_UPGRADES = 61


@dataclasses.dataclass(frozen=True)
class DecodedUpgxSection(DecodedChkSection):
    """Represent UPGx - Brood War Upgrade Settings.

    :param _uses_default_settings: u8[61]; 0=custom, 1=use SC defaults
    :param _base_mineral_cost: u16[61]
    :param _mineral_cost_factor: u16[61]
    :param _base_gas_cost: u16[61]
    :param _gas_cost_factor: u16[61]
    :param _base_research_time: u16[61]
    :param _research_time_factor: u16[61]
    """

    _uses_default_settings: list[int]
    _base_mineral_cost: list[int]
    _mineral_cost_factor: list[int]
    _base_gas_cost: list[int]
    _gas_cost_factor: list[int]
    _base_research_time: list[int]
    _research_time_factor: list[int]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.UPGX

    @property
    def uses_default_settings(self) -> list[int]:
        return self._uses_default_settings

    @property
    def base_mineral_cost(self) -> list[int]:
        return self._base_mineral_cost

    @property
    def mineral_cost_factor(self) -> list[int]:
        return self._mineral_cost_factor

    @property
    def base_gas_cost(self) -> list[int]:
        return self._base_gas_cost

    @property
    def gas_cost_factor(self) -> list[int]:
        return self._gas_cost_factor

    @property
    def base_research_time(self) -> list[int]:
        return self._base_research_time

    @property
    def research_time_factor(self) -> list[int]:
        return self._research_time_factor
