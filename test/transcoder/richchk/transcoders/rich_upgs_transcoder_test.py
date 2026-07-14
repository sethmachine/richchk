import pytest

from richchk.model.chk.upgs.decoded_upgs_section import DecodedUpgsSection
from richchk.model.richchk.richchk_decode_context import RichChkDecodeContext
from richchk.model.richchk.richchk_encode_context import RichChkEncodeContext
from richchk.model.richchk.str.rich_str_lookup import RichStrLookup
from richchk.model.richchk.upgrades.upgrade_id import UpgradeId
from richchk.transcoder.richchk.transcoders.rich_upgs_transcoder import (
    RichUpgsTranscoder,
)

_NUM_UPGRADES = 46

_EMPTY_STR_LOOKUP = RichStrLookup(_string_by_id_lookup={}, _id_by_string_lookup={})


def _make_decoded_upgs(
    uses_default: int = 1,
    base_mineral: int = 100,
    mineral_factor: int = 100,
    base_gas: int = 0,
    gas_factor: int = 0,
    base_time: int = 1800,
    time_factor: int = 0,
) -> DecodedUpgsSection:
    return DecodedUpgsSection(
        _uses_default_settings=[uses_default] * _NUM_UPGRADES,
        _base_mineral_cost=[base_mineral] * _NUM_UPGRADES,
        _mineral_cost_factor=[mineral_factor] * _NUM_UPGRADES,
        _base_gas_cost=[base_gas] * _NUM_UPGRADES,
        _gas_cost_factor=[gas_factor] * _NUM_UPGRADES,
        _base_research_time=[base_time] * _NUM_UPGRADES,
        _research_time_factor=[time_factor] * _NUM_UPGRADES,
    )


@pytest.fixture
def decode_context() -> RichChkDecodeContext:
    return RichChkDecodeContext(_rich_str_lookup=_EMPTY_STR_LOOKUP)


@pytest.fixture
def encode_context() -> RichChkEncodeContext:
    from richchk.model.richchk.mrgn.rich_mrgn_lookup import RichMrgnLookup
    from richchk.model.richchk.swnm.rich_swnm_lookup import RichSwnmLookup
    from richchk.model.richchk.uprp.rich_cuwp_lookup import RichCuwpLookup

    return RichChkEncodeContext(
        _rich_str_lookup=_EMPTY_STR_LOOKUP,
        _rich_mrgn_lookup=RichMrgnLookup(
            _location_by_id_lookup={}, _id_by_location_lookup={}
        ),
        _rich_swnm_lookup=RichSwnmLookup(
            _switch_by_id_lookup={}, _id_by_switch_lookup={}
        ),
        _rich_cuwp_lookup=RichCuwpLookup(_cuwp_by_id_lookup={}, _id_by_cuwp_lookup={}),
        _wav_metadata_lookup=None,
    )


def test_it_decodes_correct_number_of_settings(decode_context):
    decoded = _make_decoded_upgs()
    rich = RichUpgsTranscoder().decode(decoded, decode_context)
    assert len(rich.upgrade_cost_settings) == _NUM_UPGRADES


def test_it_decodes_upgrade_ids_as_keys(decode_context):
    decoded = _make_decoded_upgs()
    rich = RichUpgsTranscoder().decode(decoded, decode_context)
    assert (
        rich.upgrade_cost_settings[UpgradeId.TERRAN_INFANTRY_ARMOR].upgrade_id
        == UpgradeId.TERRAN_INFANTRY_ARMOR
    )
    assert (
        rich.upgrade_cost_settings[UpgradeId.TERRAN_VEHICLE_PLATING].upgrade_id
        == UpgradeId.TERRAN_VEHICLE_PLATING
    )


def test_it_decodes_uses_default_settings_as_bool(decode_context):
    decoded = _make_decoded_upgs(uses_default=1)
    rich = RichUpgsTranscoder().decode(decoded, decode_context)
    assert (
        rich.upgrade_cost_settings[
            UpgradeId.TERRAN_INFANTRY_ARMOR
        ].uses_default_settings
        is True
    )


def test_it_decodes_costs_correctly(decode_context):
    decoded = _make_decoded_upgs(base_mineral=200, base_gas=50)
    rich = RichUpgsTranscoder().decode(decoded, decode_context)
    assert (
        rich.upgrade_cost_settings[UpgradeId.TERRAN_INFANTRY_ARMOR].base_mineral_cost
        == 200
    )
    assert (
        rich.upgrade_cost_settings[UpgradeId.TERRAN_INFANTRY_ARMOR].base_gas_cost == 50
    )


def test_it_encodes_and_round_trips(decode_context, encode_context):
    decoded = _make_decoded_upgs()
    transcoder = RichUpgsTranscoder()
    rich = transcoder.decode(decoded, decode_context)
    re_decoded = transcoder.encode(rich, encode_context)
    assert re_decoded == decoded


def test_it_uses_encode_cache_for_same_object(decode_context, encode_context):
    decoded = _make_decoded_upgs()
    transcoder = RichUpgsTranscoder()
    rich = transcoder.decode(decoded, decode_context)
    result1 = transcoder.encode(rich, encode_context)
    result2 = transcoder.encode(rich, encode_context)
    assert result1 is result2
