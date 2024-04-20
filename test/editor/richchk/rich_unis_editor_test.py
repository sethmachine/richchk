""""""

from decimal import Decimal

from chkjson.editor.richchk.rich_unis_editor import RichUnisEditor
from chkjson.model.richchk.str.rich_string import RichString
from chkjson.model.richchk.unis.unit_id import UnitId
from chkjson.model.richchk.unis.unit_setting import UnitSetting
from chkjson.model.richchk.unis.weapon_id import WeaponId
from chkjson.model.richchk.unis.weapon_setting import WeaponSetting

from ...fixtures.unit_settings_fixtures import (
    generate_empty_rich_unis,
    generate_rich_unis_with_terran_marine_setting,
    generate_unit_setting,
)


def test_it_upserts_multiple_unit_settings():
    empty_rich_unis = generate_empty_rich_unis()
    editor = RichUnisEditor()
    new_settings = [
        generate_unit_setting(UnitId.TERRAN_MARINE),
        generate_unit_setting(UnitId.ZERG_ZERGLING),
    ]
    new_unis = editor.upsert_all_unit_settings(
        unit_settings=new_settings, unis=empty_rich_unis
    )
    for setting in new_settings:
        assert setting in new_unis.unit_settings
        assert setting not in empty_rich_unis.unit_settings


def test_it_upserts_a_single_unit_setting():
    empty_rich_unis = generate_empty_rich_unis()
    editor = RichUnisEditor()
    terran_marine_unit_setting = generate_unit_setting(UnitId.TERRAN_MARINE)
    new_unis = editor.upsert_unit_setting(
        unit_setting=terran_marine_unit_setting, unis=empty_rich_unis
    )
    assert terran_marine_unit_setting in new_unis.unit_settings
    assert terran_marine_unit_setting not in empty_rich_unis.unit_settings


def test_it_replaces_unit_setting_if_it_already_exists():
    rich_unis_with_terran_marine_setting = (
        generate_rich_unis_with_terran_marine_setting()
    )
    editor = RichUnisEditor()
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
    assert new_marine not in rich_unis_with_terran_marine_setting.unit_settings
    new_unis = editor.upsert_unit_setting(
        unit_setting=new_marine, unis=rich_unis_with_terran_marine_setting
    )
    assert new_unis.unit_settings == [new_marine]
    assert new_marine not in rich_unis_with_terran_marine_setting.unit_settings
