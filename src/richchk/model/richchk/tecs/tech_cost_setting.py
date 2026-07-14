"""Represents cost and time settings for a single technology in the TECS section."""

import dataclasses

from ..techs.tech_id import TechId


@dataclasses.dataclass(frozen=True)
class TechCostSetting:
    """Cost and time settings for a single technology.

    :param _tech_id: the tech this setting applies to
    :param _uses_default_settings: True=use SC game defaults, False=use custom values
    :param _mineral_cost: mineral cost
    :param _gas_cost: gas cost
    :param _research_time: research time (in frames)
    :param _energy_cost: energy cost to use the ability
    """

    _tech_id: TechId
    _uses_default_settings: bool
    _mineral_cost: int
    _gas_cost: int
    _research_time: int
    _energy_cost: int

    @property
    def tech_id(self) -> TechId:
        return self._tech_id

    @property
    def uses_default_settings(self) -> bool:
        return self._uses_default_settings

    @property
    def mineral_cost(self) -> int:
        return self._mineral_cost

    @property
    def gas_cost(self) -> int:
        return self._gas_cost

    @property
    def research_time(self) -> int:
        return self._research_time

    @property
    def energy_cost(self) -> int:
        return self._energy_cost
