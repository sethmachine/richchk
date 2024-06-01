""""""

from decimal import Decimal

from richchk.editor.richchk.rich_unix_editor import RichUnixEditor
from richchk.model.richchk.str.rich_string import RichString
from richchk.model.richchk.unis.unit_id import UnitId
from richchk.model.richchk.unis.unit_setting import UnitSetting
from richchk.model.richchk.unis.weapon_id import WeaponId
from richchk.model.richchk.unis.weapon_setting import WeaponSetting

from ...fixtures.unit_settings_fixtures import (
    generate_empty_rich_unix,
    generate_rich_unix_with_terran_marine_setting,
    generate_unit_setting,
)


def test_it_replaces_rich_chk_section():
    empty_rich_unix = generate_empty_rich_unix()
    editor = RichUnixEditor()
    new_settings = [
        generate_unit_setting(UnitId.TERRAN_MARINE),
        generate_unit_setting(UnitId.ZERG_ZERGLING),
    ]
    new_unis = editor.upsert_all_unit_settings(
        unit_settings=new_settings, unis=empty_rich_unix
    )
    for setting in new_settings:
        assert setting in new_unis.unit_settings
        assert setting not in empty_rich_unix.unit_settings


def test_it_upserts_multiple_unit_settings():
    empty_rich_unix = generate_empty_rich_unix()
    editor = RichUnixEditor()
    new_settings = [
        generate_unit_setting(UnitId.TERRAN_MARINE),
        generate_unit_setting(UnitId.ZERG_ZERGLING),
    ]
    new_unis = editor.upsert_all_unit_settings(
        unit_settings=new_settings, unis=empty_rich_unix
    )
    for setting in new_settings:
        assert setting in new_unis.unit_settings
        assert setting not in empty_rich_unix.unit_settings


def test_it_upserts_a_single_unit_setting():
    empty_rich_unix = generate_empty_rich_unix()
    editor = RichUnixEditor()
    terran_marine_unit_setting = generate_unit_setting(UnitId.TERRAN_MARINE)
    new_unis = editor.upsert_unit_setting(
        unit_setting=terran_marine_unit_setting, unis=empty_rich_unix
    )
    assert terran_marine_unit_setting in new_unis.unit_settings
    assert terran_marine_unit_setting not in empty_rich_unix.unit_settings


def test_it_replaces_unit_setting_if_it_already_exists():
    rich_unix_with_terran_marine_setting = (
        generate_rich_unix_with_terran_marine_setting()
    )
    editor = RichUnixEditor()
    new_marine = UnitSetting(
        _unit_id=UnitId.TERRAN_MARINE,
        _hitpoints=Decimal(1000),
        _shieldpoints=1000,
        _armorpoints=1000,
        _build_time=1000,
        _mineral_cost=1000,
        _gas_cost=1000,
        _custom_unit_name=RichString(_value="Custom terran marine?"),
        _weapons=[
            WeaponSetting(
                _weapon_id=WeaponId.GAUSS_RIFLE_NORMAL,
                _base_damage=1000,
                _upgrade_damage=1000,
            )
        ],
        _use_default_unit_settings=False,
    )
    assert new_marine not in rich_unix_with_terran_marine_setting.unit_settings
    new_unis = editor.upsert_unit_setting(
        unit_setting=new_marine, unis=rich_unix_with_terran_marine_setting
    )
    assert new_unis.unit_settings == [new_marine]
    assert new_marine not in rich_unix_with_terran_marine_setting.unit_settings
