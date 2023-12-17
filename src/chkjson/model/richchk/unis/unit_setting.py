"""Represents a single modified unit setting for an entry in UNIS or UNIX."""

import dataclasses

from ..str.rich_string import RichString
from .unit_id import UnitId


@dataclasses.dataclass(frozen=True)
class UnitSetting:
    _unit_id: UnitId
    _hitpoints: int
    _shieldpoints: int
    _armorpoints: int
    _build_time: int
    _mineral_cost: int
    _gas_cost: int
    _custom_unit_name: RichString
    _base_damage: int
    _upgrade_damage: int

    @property
    def unit_id(self) -> UnitId:
        return self._unit_id

    @property
    def hitpoints(self) -> int:
        return self._hitpoints

    @property
    def shieldpoints(self) -> int:
        return self._shieldpoints

    @property
    def armorpoints(self) -> int:
        return self._armorpoints

    @property
    def build_time(self) -> int:
        return self._build_time

    @property
    def mineral_cost(self) -> int:
        return self._mineral_cost

    @property
    def gas_cost(self) -> int:
        return self._gas_cost

    @property
    def custom_unit_name(self) -> RichString:
        return self._custom_unit_name

    @property
    def base_damage(self) -> int:
        return self._base_damage

    @property
    def upgrade_damage(self) -> int:
        return self._upgrade_damage
