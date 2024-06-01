"""Represents a single modified unit setting for an entry in UNIS or UNIX.

It is possible for a map to save custom settings to the UNIS setting but set the unit
default settings flag to 1.  Starcraft will ignore the custom settings but the UNIS
still store the unused data.  The field `UnitSetting#use_default_unit_settings` will
indicate whether this is the case.
"""

import dataclasses
from decimal import Decimal

from ..str.rich_string import RichString
from .unit_id import UnitId
from .weapon_setting import WeaponSetting


@dataclasses.dataclass(frozen=True)
class UnitSetting:
    _unit_id: UnitId
    # it is possible to have values less than 256
    # or not a multiple of 256 in the DecodedUnis
    _hitpoints: Decimal
    _shieldpoints: int
    _armorpoints: int
    _build_time: int
    _mineral_cost: int
    _gas_cost: int
    _custom_unit_name: RichString
    _weapons: list[WeaponSetting]
    _use_default_unit_settings: bool = False

    @property
    def use_default_unit_settings(self) -> bool:
        return self._use_default_unit_settings

    @property
    def unit_id(self) -> UnitId:
        return self._unit_id

    @property
    def hitpoints(self) -> Decimal:
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
        return self._weapons
