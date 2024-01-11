"""This is really an integration test as it relies on the UNIS transcoder."""
import pytest

from chkjson.model.chk.unis.decoded_unis_section import DecodedUnisSection
from chkjson.model.richchk.richchk_decode_context import RichChkDecodeContext
from chkjson.model.richchk.str.rich_str_lookup import RichStrLookup
from chkjson.model.richchk.str.rich_string import RichNullString, RichString
from chkjson.model.richchk.unis.unit_id import UnitId
from chkjson.model.richchk.unis.weapon_id import WeaponId
from chkjson.model.richchk.unis.weapon_setting import WeaponSetting
from chkjson.transcoder.chk.transcoders.chk_unis_transcoder import ChkUnisTranscoder
from chkjson.transcoder.richchk.transcoders.richchk_unis_transcoder import (
    RichChkUnisTranscoder,
)

from ....chk_resources import CHK_SECTION_FILE_PATHS

# these units were modified so they don't use the default settings flags
# [TERRAN_MARINE, TERRAN_GHOST, TERRAN_FIREBAT]
_MODIFIED_UNIT_IDS = [0, 1, 32]
# this unit and weapons was modified manually in a GUI map editor
_TERRAN_MARINE_UNIT_ID = 0
_TERRAN_GAUSS_RIFLE_ID = 0

# the terran marine was modified to these unit settings in a GUI map editor
_TERRAN_MARINE_HITPOINTS = 100 * 256  # hitpoints are stored as 1/256 hitpoints
_TERRAN_MARINE_ARMORPOINTS = 100
_TERRAN_MARINE_BUILD_TIME = 100  # build time is stored as 1/60 seconds
_TERRAIN_MARINE_MINERAL_COST = 100
_TERRAIN_MARINE_GAS_COST = 100
_TERRAN_MARINE_GAUSS_WEAPON_BASE_DAMAGE = 100
_TERRAN_MARINE_GAUSS_WEAPON_UPGRADE_DAMAGE = 100


def _read_chk_section() -> bytes:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedUnisSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return chk_binary_data


def _get_unit_setting_by_unit_id(rich_unis, unit_id):
    maybe_unit_setting = [x for x in rich_unis.unit_settings if x.unit_id == unit_id]
    if not maybe_unit_setting:
        return None
    return maybe_unit_setting[0]


@pytest.fixture
def rich_chk_decode_context():
    return RichChkDecodeContext(
        _rich_str_lookup=RichStrLookup(
            {123: RichString(_value="custom terran marine name")}
        )
    )


@pytest.fixture
def decoded_unis_section_with_custom_terran_marine():
    return DecodedUnisSection(
        _unit_default_settings_flags=[0] + ([1] * (len(UnitId) - 1)),
        _unit_hitpoints=[100 * 256] + ([0] * (len(UnitId) - 1)),
        _unit_shieldpoints=[1337] + ([0] * (len(UnitId) - 1)),
        _unit_armorpoints=[125] + ([0] * (len(UnitId) - 1)),
        _unit_build_times=[60] + ([0] * (len(UnitId) - 1)),
        _unit_mineral_costs=[25] + ([0] * (len(UnitId) - 1)),
        _unit_gas_costs=[75] + ([0] * (len(UnitId) - 1)),
        _unit_string_ids=[123] + ([0] * (len(UnitId) - 1)),
        # unit ID 0 (marine) also happens to use weapon ID 0 (gauss rifle)
        _unit_base_weapon_damages=[100] + ([0] * (len(WeaponId) - 1)),
        _unit_upgrade_weapon_damages=[10] + ([0] * (len(WeaponId) - 1)),
    )


@pytest.fixture
def decoded_unis_section_with_custom_terran_marine_no_custom_name():
    return DecodedUnisSection(
        _unit_default_settings_flags=[0] + ([1] * (len(UnitId) - 1)),
        _unit_hitpoints=[100 * 256] + ([0] * (len(UnitId) - 1)),
        _unit_shieldpoints=[1337] + ([0] * (len(UnitId) - 1)),
        _unit_armorpoints=[125] + ([0] * (len(UnitId) - 1)),
        _unit_build_times=[60] + ([0] * (len(UnitId) - 1)),
        _unit_mineral_costs=[25] + ([0] * (len(UnitId) - 1)),
        _unit_gas_costs=[75] + ([0] * (len(UnitId) - 1)),
        _unit_string_ids=[0] * len(UnitId),
        # unit ID 0 (marine) also happens to use weapon ID 0 (gauss rifle)
        _unit_base_weapon_damages=[100] + ([0] * (len(WeaponId) - 1)),
        _unit_upgrade_weapon_damages=[10] + ([0] * (len(WeaponId) - 1)),
    )


@pytest.fixture
def decoded_unis_section_with_terran_science_vessel_no_weapon():
    return DecodedUnisSection(
        # terran science vessel is the first unit without a weapon
        _unit_default_settings_flags=([1] * 9) + [0] + [1] * (len(UnitId) - 10),
        _unit_hitpoints=[0] * len(UnitId),
        _unit_shieldpoints=[0] * len(UnitId),
        _unit_armorpoints=[0] * len(UnitId),
        _unit_build_times=[0] * len(UnitId),
        _unit_mineral_costs=[0] * len(UnitId),
        _unit_gas_costs=[0] * len(UnitId),
        _unit_string_ids=[0] * len(UnitId),
        _unit_base_weapon_damages=[0] * len(WeaponId),
        _unit_upgrade_weapon_damages=[0] * len(WeaponId),
    )


@pytest.fixture
def decoded_unis_section_with_no_modified_units():
    return DecodedUnisSection(
        _unit_default_settings_flags=[1] * len(UnitId),
        _unit_hitpoints=[0] * len(UnitId),
        _unit_shieldpoints=[0] * len(UnitId),
        _unit_armorpoints=[0] * len(UnitId),
        _unit_build_times=[0] * len(UnitId),
        _unit_mineral_costs=[0] * len(UnitId),
        _unit_gas_costs=[0] * len(UnitId),
        _unit_string_ids=[0] * len(UnitId),
        _unit_base_weapon_damages=[0] * len(WeaponId),
        _unit_upgrade_weapon_damages=[0] * len(WeaponId),
    )


def test_it_decodes_rich_unis_with_expected_unit_settings(
    rich_chk_decode_context, decoded_unis_section_with_custom_terran_marine
):
    rich_transcoder = RichChkUnisTranscoder()
    rich_unis = rich_transcoder.decode(
        decoded_chk_section=decoded_unis_section_with_custom_terran_marine,
        rich_chk_decode_context=rich_chk_decode_context,
    )
    assert len(rich_unis.unit_settings) == 1
    assert rich_unis.unit_settings[0].unit_id == UnitId.get_by_id(0)
    assert rich_unis.unit_settings[0].hitpoints == 100
    assert rich_unis.unit_settings[0].shieldpoints == 1337
    assert rich_unis.unit_settings[0].armorpoints == 125
    assert rich_unis.unit_settings[0].build_time == 60
    assert rich_unis.unit_settings[0].mineral_cost == 25
    assert rich_unis.unit_settings[0].gas_cost == 75
    assert rich_unis.unit_settings[
        0
    ].custom_unit_name == rich_chk_decode_context.rich_str_lookup.get_string_by_id(123)
    assert rich_unis.unit_settings[0].weapons == [
        WeaponSetting(
            _weapon_id=WeaponId.get_by_id(0), _base_damage=100, _upgrade_damage=10
        )
    ]


def test_it_decodes_rich_unis_with_null_string_for_unit(
    rich_chk_decode_context,
    decoded_unis_section_with_custom_terran_marine_no_custom_name,
):
    rich_transcoder = RichChkUnisTranscoder()
    rich_unis = rich_transcoder.decode(
        decoded_chk_section=decoded_unis_section_with_custom_terran_marine_no_custom_name,  # noqa: E501
        rich_chk_decode_context=rich_chk_decode_context,
    )
    assert len(rich_unis.unit_settings) == 1
    assert rich_unis.unit_settings[0].unit_id == UnitId.get_by_id(0)
    assert rich_unis.unit_settings[0].hitpoints == 100
    assert rich_unis.unit_settings[0].shieldpoints == 1337
    assert rich_unis.unit_settings[0].armorpoints == 125
    assert rich_unis.unit_settings[0].build_time == 60
    assert rich_unis.unit_settings[0].mineral_cost == 25
    assert rich_unis.unit_settings[0].gas_cost == 75
    assert rich_unis.unit_settings[0].custom_unit_name == RichNullString()
    assert rich_unis.unit_settings[0].weapons == [
        WeaponSetting(
            _weapon_id=WeaponId.get_by_id(0), _base_damage=100, _upgrade_damage=10
        )
    ]


def test_it_decodes_rich_unis_for_unit_without_weapons(
    rich_chk_decode_context,
    decoded_unis_section_with_terran_science_vessel_no_weapon,
):
    rich_transcoder = RichChkUnisTranscoder()
    rich_unis = rich_transcoder.decode(
        decoded_chk_section=decoded_unis_section_with_terran_science_vessel_no_weapon,
        rich_chk_decode_context=rich_chk_decode_context,
    )
    assert len(rich_unis.unit_settings) == 1
    assert rich_unis.unit_settings[0].custom_unit_name == RichNullString()
    assert rich_unis.unit_settings[0].weapons == []


def test_it_decodes_empty_rich_unis_if_no_modified_units(
    decoded_unis_section_with_no_modified_units,
):
    rich_transcoder = RichChkUnisTranscoder()
    rich_unis = rich_transcoder.decode(
        decoded_chk_section=decoded_unis_section_with_no_modified_units,
        rich_chk_decode_context=RichChkDecodeContext(
            _rich_str_lookup=RichStrLookup({})
        ),
    )
    assert len(rich_unis.unit_settings) == 0


def test_integration_it_decodes_rich_unis_with_expected_unit_settings():
    transcoder: ChkUnisTranscoder = ChkUnisTranscoder()
    chk_binary_data = _read_chk_section()
    decoded_unis: DecodedUnisSection = transcoder.decode(chk_binary_data)
    rich_transcoder = RichChkUnisTranscoder()
    rich_unis = rich_transcoder.decode(
        decoded_chk_section=decoded_unis,
        rich_chk_decode_context=RichChkDecodeContext(
            _rich_str_lookup=RichStrLookup(_string_by_id_lookup={})
        ),
    )
    for expected_unit_id in _MODIFIED_UNIT_IDS:
        assert (
            _get_unit_setting_by_unit_id(rich_unis, UnitId.get_by_id(expected_unit_id))
            is not None
        )
    terran_marine = _get_unit_setting_by_unit_id(rich_unis, UnitId.TERRAN_MARINE)
    assert terran_marine.hitpoints == _TERRAN_MARINE_HITPOINTS // 256
    assert terran_marine.armorpoints == _TERRAN_MARINE_ARMORPOINTS
    assert terran_marine.build_time == _TERRAN_MARINE_BUILD_TIME
    assert terran_marine.mineral_cost == _TERRAIN_MARINE_MINERAL_COST
    assert terran_marine.gas_cost == _TERRAIN_MARINE_GAS_COST
    assert len(terran_marine.weapons) == 1
    gauss_rifle = terran_marine.weapons[0]
    assert gauss_rifle.weapon_id == WeaponId.GAUSS_RIFLE_NORMAL
    assert gauss_rifle.base_damage == _TERRAN_MARINE_GAUSS_WEAPON_BASE_DAMAGE
    assert gauss_rifle.upgrade_damage == _TERRAN_MARINE_GAUSS_WEAPON_UPGRADE_DAMAGE
