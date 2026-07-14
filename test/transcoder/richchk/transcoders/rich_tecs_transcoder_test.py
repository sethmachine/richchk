import pytest

from richchk.model.chk.tecs.decoded_tecs_section import DecodedTecsSection
from richchk.model.richchk.richchk_decode_context import RichChkDecodeContext
from richchk.model.richchk.richchk_encode_context import RichChkEncodeContext
from richchk.model.richchk.str.rich_str_lookup import RichStrLookup
from richchk.model.richchk.techs.tech_id import TechId
from richchk.transcoder.richchk.transcoders.rich_tecs_transcoder import (
    RichTecsTranscoder,
)

_NUM_TECHS = 24

_EMPTY_STR_LOOKUP = RichStrLookup(_string_by_id_lookup={}, _id_by_string_lookup={})


def _make_decoded_tecs(
    uses_default: int = 1,
    mineral: int = 100,
    gas: int = 0,
    time: int = 1800,
    energy: int = 0,
) -> DecodedTecsSection:
    return DecodedTecsSection(
        _uses_default_settings=[uses_default] * _NUM_TECHS,
        _mineral_cost=[mineral] * _NUM_TECHS,
        _gas_cost=[gas] * _NUM_TECHS,
        _research_time=[time] * _NUM_TECHS,
        _energy_cost=[energy] * _NUM_TECHS,
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
    decoded = _make_decoded_tecs()
    rich = RichTecsTranscoder().decode(decoded, decode_context)
    assert len(rich.tech_cost_settings) == _NUM_TECHS


def test_it_decodes_tech_ids_in_order(decode_context):
    decoded = _make_decoded_tecs()
    rich = RichTecsTranscoder().decode(decoded, decode_context)
    assert rich.tech_cost_settings[0].tech_id == TechId.STIM_PACKS
    assert rich.tech_cost_settings[1].tech_id == TechId.LOCKDOWN


def test_it_decodes_uses_default_settings_as_bool(decode_context):
    decoded = _make_decoded_tecs(uses_default=1)
    rich = RichTecsTranscoder().decode(decoded, decode_context)
    assert rich.tech_cost_settings[0].uses_default_settings is True


def test_it_decodes_costs_correctly(decode_context):
    decoded = _make_decoded_tecs(mineral=200, gas=100, time=3600, energy=75)
    rich = RichTecsTranscoder().decode(decoded, decode_context)
    setting = rich.tech_cost_settings[0]
    assert setting.mineral_cost == 200
    assert setting.gas_cost == 100
    assert setting.research_time == 3600
    assert setting.energy_cost == 75


def test_it_encodes_and_round_trips(decode_context, encode_context):
    decoded = _make_decoded_tecs()
    transcoder = RichTecsTranscoder()
    rich = transcoder.decode(decoded, decode_context)
    re_decoded = transcoder.encode(rich, encode_context)
    assert re_decoded == decoded


def test_it_uses_encode_cache_for_same_object(decode_context, encode_context):
    decoded = _make_decoded_tecs()
    transcoder = RichTecsTranscoder()
    rich = transcoder.decode(decoded, decode_context)
    result1 = transcoder.encode(rich, encode_context)
    result2 = transcoder.encode(rich, encode_context)
    assert result1 is result2
