from richchk.model.chk.unix.decoded_unix_section import DecodedUnixSection
from richchk.model.richchk.unis.unit_id import UnitId
from richchk.model.richchk.unis.weapon_id import WeaponId
from richchk.transcoder.chk.transcoders.chk_unix_transcoder import ChkUnixTranscoder

from ....chk_resources import CHK_SECTION_FILE_PATHS

# these units were modified so they don't use the default settings flags
# [TERRAN_MARINE, TERRAN_GHOST, TERRAN_FIREBAT, TERRAN_VALKRYIE]
_MODIFIED_UNITS = [0, 1, 32, UnitId.TERRAN_VALKYRIE_FRIGATE.id]
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

_TERRAN_VALK_WEAPON_BASE_DAMAGE = 100
_TERRAN_VALK_WEAPON_UPGRADE_DAMAGE = 10


def _read_chk_section() -> bytes:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedUnixSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return chk_binary_data


def test_it_decodes_unis_chk_section_with_expected_unit_settings():
    transcoder: ChkUnixTranscoder = ChkUnixTranscoder()
    chk_binary_data = _read_chk_section()
    unis_section: DecodedUnixSection = transcoder.decode(chk_binary_data)
    for modified_unit_id in _MODIFIED_UNITS:
        assert unis_section.unit_default_settings_flags[modified_unit_id] == 0
    _assert_terran_marine_has_modified_values(unis_section)


def test_it_decodes_and_encodes_without_changing_data():
    transcoder: ChkUnixTranscoder = ChkUnixTranscoder()
    chk_binary_data = _read_chk_section()
    unis_section: DecodedUnixSection = transcoder.decode(chk_binary_data)
    _assert_terran_marine_has_modified_values(unis_section)
    actual_encoded_data = transcoder.encode(unis_section, include_header=False)
    assert actual_encoded_data == chk_binary_data
    assert transcoder.decode(actual_encoded_data) == transcoder.decode(chk_binary_data)
    _assert_terran_marine_has_modified_values(transcoder.decode(actual_encoded_data))
    _assert_terran_valkyrie_has_modified_values(transcoder.decode(actual_encoded_data))


def _assert_terran_marine_has_modified_values(unis_section: DecodedUnixSection):
    assert (
        unis_section.unit_hitpoints[_TERRAN_MARINE_UNIT_ID] == _TERRAN_MARINE_HITPOINTS
    )
    assert (
        unis_section.unit_armorpoints[_TERRAN_MARINE_UNIT_ID]
        == _TERRAN_MARINE_ARMORPOINTS
    )
    assert (
        unis_section.unit_build_times[_TERRAN_MARINE_UNIT_ID]
        == _TERRAN_MARINE_BUILD_TIME
    )
    assert (
        unis_section.unit_mineral_costs[_TERRAN_MARINE_UNIT_ID]
        == _TERRAIN_MARINE_MINERAL_COST
    )
    assert (
        unis_section.unit_gas_costs[_TERRAN_MARINE_UNIT_ID] == _TERRAIN_MARINE_GAS_COST
    )
    assert (
        unis_section.unit_base_weapon_damages[_TERRAN_GAUSS_RIFLE_ID]
        == _TERRAN_MARINE_GAUSS_WEAPON_BASE_DAMAGE
    )
    assert (
        unis_section.unit_upgrade_weapon_damages[_TERRAN_GAUSS_RIFLE_ID]
        == _TERRAN_MARINE_GAUSS_WEAPON_UPGRADE_DAMAGE
    )


def _assert_terran_valkyrie_has_modified_values(unis_section: DecodedUnixSection):
    assert (
        unis_section.unit_base_weapon_damages[WeaponId.HALO_ROCKETS.id]
        == _TERRAN_VALK_WEAPON_BASE_DAMAGE
    )
    assert (
        unis_section.unit_upgrade_weapon_damages[WeaponId.HALO_ROCKETS.id]
        == _TERRAN_VALK_WEAPON_UPGRADE_DAMAGE
    )
