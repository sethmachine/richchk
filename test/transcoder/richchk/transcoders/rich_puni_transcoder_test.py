import pytest

from richchk.model.chk.puni.decoded_puni_section import DecodedPuniSection
from richchk.model.richchk.richchk_decode_context import RichChkDecodeContext
from richchk.model.richchk.richchk_encode_context import RichChkEncodeContext
from richchk.model.richchk.str.rich_str_lookup import RichStrLookup
from richchk.transcoder.richchk.transcoders.rich_puni_transcoder import (
    RichPuniTranscoder,
)

_NUM_PLAYERS = 12
_NUM_UNITS = 228
_PLAYER_UNITS_SIZE = _NUM_PLAYERS * _NUM_UNITS

_EMPTY_STR_LOOKUP = RichStrLookup(_string_by_id_lookup={}, _id_by_string_lookup={})


def _make_decoded_puni(
    player_availability: int = 1,
    global_availability: int = 1,
    player_defaults: int = 1,
) -> DecodedPuniSection:
    return DecodedPuniSection(
        _player_unit_availability=[player_availability] * _PLAYER_UNITS_SIZE,
        _global_unit_availability=[global_availability] * _NUM_UNITS,
        _player_uses_defaults=[player_defaults] * _PLAYER_UNITS_SIZE,
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


def test_it_decodes_player_unit_availability_as_2d(decode_context):
    decoded = _make_decoded_puni(player_availability=1)
    rich = RichPuniTranscoder().decode(decoded, decode_context)
    assert len(rich.player_unit_availability) == _NUM_PLAYERS
    assert len(rich.player_unit_availability[0]) == _NUM_UNITS
    assert rich.player_unit_availability[0][0] is True


def test_it_decodes_global_unit_availability(decode_context):
    decoded = _make_decoded_puni(global_availability=0)
    rich = RichPuniTranscoder().decode(decoded, decode_context)
    assert len(rich.global_unit_availability) == _NUM_UNITS
    assert rich.global_unit_availability[0] is False


def test_it_decodes_player_uses_defaults(decode_context):
    decoded = _make_decoded_puni(player_defaults=1)
    rich = RichPuniTranscoder().decode(decoded, decode_context)
    assert len(rich.player_uses_defaults) == _NUM_PLAYERS
    assert rich.player_uses_defaults[0][0] is True


def test_it_encodes_and_round_trips(decode_context, encode_context):
    decoded = _make_decoded_puni()
    transcoder = RichPuniTranscoder()
    rich = transcoder.decode(decoded, decode_context)
    re_decoded = transcoder.encode(rich, encode_context)
    assert re_decoded == decoded


def test_it_uses_encode_cache_for_same_object(decode_context, encode_context):
    decoded = _make_decoded_puni()
    transcoder = RichPuniTranscoder()
    rich = transcoder.decode(decoded, decode_context)
    result1 = transcoder.encode(rich, encode_context)
    result2 = transcoder.encode(rich, encode_context)
    assert result1 is result2
