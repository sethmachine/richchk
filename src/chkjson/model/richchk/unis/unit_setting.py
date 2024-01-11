"""Represents a single modified unit setting for an entry in UNIS or UNIX."""

import copy
import dataclasses

from ..str.rich_string import RichString
from .unit_id import UnitId
from .weapon_setting import WeaponSetting


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
    _weapons: list[WeaponSetting]

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
    def weapons(self) -> list[WeaponSetting]:
        return copy.deepcopy(self._weapons)
