"""Represents cost and time settings for a single upgrade in the UPGS section."""

import dataclasses

from ..upgrades.upgrade_id import UpgradeId


@dataclasses.dataclass(frozen=True)
class UpgradeCostSetting:
    """Cost and time settings for a single upgrade.

    :param _upgrade_id: the upgrade this setting applies to
    :param _uses_default_settings: True=use SC game defaults, False=use custom values
    :param _base_mineral_cost: base mineral cost
    :param _mineral_cost_factor: mineral cost per level factor
    :param _base_gas_cost: base gas cost
    :param _gas_cost_factor: gas cost per level factor
    :param _base_research_time: base research time (in frames)
    :param _research_time_factor: research time per level factor
    """

    _upgrade_id: UpgradeId
    _uses_default_settings: bool
    _base_mineral_cost: int
    _mineral_cost_factor: int
    _base_gas_cost: int
    _gas_cost_factor: int
    _base_research_time: int
    _research_time_factor: int

    @property
    def upgrade_id(self) -> UpgradeId:
        return self._upgrade_id

    @property
    def uses_default_settings(self) -> bool:
        return self._uses_default_settings

    @property
    def base_mineral_cost(self) -> int:
        return self._base_mineral_cost

    @property
    def mineral_cost_factor(self) -> int:
        return self._mineral_cost_factor

    @property
    def base_gas_cost(self) -> int:
        return self._base_gas_cost

    @property
    def gas_cost_factor(self) -> int:
        return self._gas_cost_factor

    @property
    def base_research_time(self) -> int:
        return self._base_research_time

    @property
    def research_time_factor(self) -> int:
        return self._research_time_factor
