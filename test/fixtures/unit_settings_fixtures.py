""""""

from decimal import Decimal

from richchk.model.richchk.str.rich_string import RichString
from richchk.model.richchk.unis.rich_unis_section import RichUnisSection
from richchk.model.richchk.unis.unit_id import UnitId
from richchk.model.richchk.unis.unit_setting import UnitSetting
from richchk.model.richchk.unis.weapon_id import WeaponId
from richchk.model.richchk.unis.weapon_setting import WeaponSetting
from richchk.model.richchk.unix.rich_unix_section import RichUnixSection


def generate_unit_setting(unit_id: UnitId) -> UnitSetting:
    return UnitSetting(
        _unit_id=unit_id,
        _hitpoints=Decimal(100),
        _shieldpoints=100,
        _armorpoints=100,
        _build_time=100,
        _mineral_cost=100,
        _gas_cost=100,
        _custom_unit_name=RichString(_value="Custom terran marine"),
        _weapons=[
            WeaponSetting(
                _weapon_id=WeaponId.GAUSS_RIFLE_NORMAL,
                _base_damage=100,
                _upgrade_damage=100,
            )
        ],
        _use_default_unit_settings=False,
    )


def generate_empty_rich_unix() -> RichUnixSection:
    return RichUnixSection(_unit_settings=[])


def generate_rich_unix_with_terran_marine_setting() -> RichUnixSection:
    return RichUnixSection(_unit_settings=[generate_unit_setting(UnitId.TERRAN_MARINE)])


def generate_empty_rich_unis() -> RichUnisSection:
    return RichUnisSection(_unit_settings=[])


def generate_rich_unis_with_terran_marine_setting() -> RichUnisSection:
    return RichUnisSection(_unit_settings=[generate_unit_setting(UnitId.TERRAN_MARINE)])
