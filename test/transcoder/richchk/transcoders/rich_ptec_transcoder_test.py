import pytest

from richchk.model.chk.ptec.decoded_ptec_section import DecodedPtecSection
from richchk.model.richchk.richchk_decode_context import RichChkDecodeContext
from richchk.model.richchk.richchk_encode_context import RichChkEncodeContext
from richchk.model.richchk.str.rich_str_lookup import RichStrLookup
from richchk.model.richchk.techs.tech_id import TechId
from richchk.model.richchk.trig.player_id import PlayerId
from richchk.transcoder.richchk.transcoders.rich_ptec_transcoder import (
    RichPtecTranscoder,
)

_NUM_PLAYERS = 12
_NUM_TECHS = 24
_PLAYER_TECHS_SIZE = _NUM_PLAYERS * _NUM_TECHS

_EMPTY_STR_LOOKUP = RichStrLookup(_string_by_id_lookup={}, _id_by_string_lookup={})


def _make_decoded_ptec(
    player_avail: int = 1,
    player_researched: int = 0,
    global_avail: int = 1,
    global_researched: int = 0,
    player_defaults: int = 1,
) -> DecodedPtecSection:
    return DecodedPtecSection(
        _player_tech_availability=[player_avail] * _PLAYER_TECHS_SIZE,
        _player_tech_researched=[player_researched] * _PLAYER_TECHS_SIZE,
        _global_tech_availability=[global_avail] * _NUM_TECHS,
        _global_tech_researched=[global_researched] * _NUM_TECHS,
        _player_uses_defaults=[player_defaults] * _PLAYER_TECHS_SIZE,
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


def test_it_decodes_player_tech_availability_as_dict(decode_context):
    decoded = _make_decoded_ptec(player_avail=1)
    rich = RichPtecTranscoder().decode(decoded, decode_context)
    assert len(rich.player_tech_availability) == _NUM_PLAYERS
    assert len(rich.player_tech_availability[PlayerId.PLAYER_1]) == _NUM_TECHS
    assert rich.player_tech_availability[PlayerId.PLAYER_1][TechId.STIM_PACKS] is True


def test_it_decodes_global_tech_availability(decode_context):
    decoded = _make_decoded_ptec(global_avail=0)
    rich = RichPtecTranscoder().decode(decoded, decode_context)
    assert rich.global_tech_availability[TechId.STIM_PACKS] is False


def test_it_decodes_player_tech_researched(decode_context):
    decoded = _make_decoded_ptec(player_researched=1)
    rich = RichPtecTranscoder().decode(decoded, decode_context)
    assert rich.player_tech_researched[PlayerId.PLAYER_1][TechId.STIM_PACKS] is True


def test_it_encodes_and_round_trips(decode_context, encode_context):
    decoded = _make_decoded_ptec()
    transcoder = RichPtecTranscoder()
    rich = transcoder.decode(decoded, decode_context)
    re_decoded = transcoder.encode(rich, encode_context)
    assert re_decoded == decoded


def test_it_uses_encode_cache_for_same_object(decode_context, encode_context):
    decoded = _make_decoded_ptec()
    transcoder = RichPtecTranscoder()
    rich = transcoder.decode(decoded, decode_context)
    result1 = transcoder.encode(rich, encode_context)
    result2 = transcoder.encode(rich, encode_context)
    assert result1 is result2
