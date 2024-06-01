"""Represent the base damage and upgrade bonus damage of a single weapon."""

import dataclasses

from .weapon_id import WeaponId


@dataclasses.dataclass(frozen=True)
class WeaponSetting:
    _weapon_id: WeaponId
    _base_damage: int
    _upgrade_damage: int

    @property
    def weapon_id(self) -> WeaponId:
        return self._weapon_id

    @property
    def base_damage(self) -> int:
        return self._base_damage

    @property
    def upgrade_damage(self) -> int:
        return self._upgrade_damage
