"""TECS - Classic Tech Settings (global cost overrides).

u8[24]  uses_default_settings: 0=uses custom, 1=uses SC game defaults u16[24]
mineral_cost:          mineral cost per tech u16[24] gas_cost:              gas cost per
tech u16[24] research_time:         research time per tech u16[24] energy_cost: energy
cost per tech

Total: 24 + 4*(2*24) = 24 + 192 = 216 bytes.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..decoded_chk_section import DecodedChkSection

_NUM_TECHS = 24


@dataclasses.dataclass(frozen=True)
class DecodedTecsSection(DecodedChkSection):
    """Represent TECS - Classic Tech Settings.

    :param _uses_default_settings: u8[24]; 0=custom, 1=use SC defaults
    :param _mineral_cost: u16[24]
    :param _gas_cost: u16[24]
    :param _research_time: u16[24]
    :param _energy_cost: u16[24]
    """

    _uses_default_settings: list[int]
    _mineral_cost: list[int]
    _gas_cost: list[int]
    _research_time: list[int]
    _energy_cost: list[int]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.TECS

    @property
    def uses_default_settings(self) -> list[int]:
        return self._uses_default_settings

    @property
    def mineral_cost(self) -> list[int]:
        return self._mineral_cost

    @property
    def gas_cost(self) -> list[int]:
        return self._gas_cost

    @property
    def research_time(self) -> list[int]:
        return self._research_time

    @property
    def energy_cost(self) -> list[int]:
        return self._energy_cost
