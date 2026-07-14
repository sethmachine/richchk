import pytest

from richchk.model.chk.upgr.decoded_upgr_section import DecodedUpgrSection
from richchk.model.richchk.richchk_decode_context import RichChkDecodeContext
from richchk.model.richchk.richchk_encode_context import RichChkEncodeContext
from richchk.model.richchk.str.rich_str_lookup import RichStrLookup
from richchk.model.richchk.trig.player_id import PlayerId
from richchk.model.richchk.upgrades.upgrade_id import UpgradeId
from richchk.transcoder.richchk.transcoders.rich_upgr_transcoder import (
    RichUpgrTranscoder,
)

_NUM_PLAYERS = 12
_NUM_UPGRADES = 46
_PLAYER_UPGRADES_SIZE = _NUM_PLAYERS * _NUM_UPGRADES

_EMPTY_STR_LOOKUP = RichStrLookup(_string_by_id_lookup={}, _id_by_string_lookup={})


def _make_decoded_upgr(
    player_max: int = 3,
    player_start: int = 0,
    global_max: int = 3,
    global_start: int = 0,
    player_defaults: int = 1,
) -> DecodedUpgrSection:
    return DecodedUpgrSection(
        _player_max_levels=[player_max] * _PLAYER_UPGRADES_SIZE,
        _player_start_levels=[player_start] * _PLAYER_UPGRADES_SIZE,
        _global_max_levels=[global_max] * _NUM_UPGRADES,
        _global_start_levels=[global_start] * _NUM_UPGRADES,
        _player_uses_defaults=[player_defaults] * _PLAYER_UPGRADES_SIZE,
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


def test_it_decodes_player_max_levels_as_dict(decode_context):
    decoded = _make_decoded_upgr(player_max=3)
    rich = RichUpgrTranscoder().decode(decoded, decode_context)
    assert len(rich.player_max_levels) == _NUM_PLAYERS
    assert len(rich.player_max_levels[PlayerId.PLAYER_1]) == _NUM_UPGRADES
    assert (
        rich.player_max_levels[PlayerId.PLAYER_1][UpgradeId.TERRAN_INFANTRY_ARMOR] == 3
    )


def test_it_decodes_global_levels(decode_context):
    decoded = _make_decoded_upgr(global_max=2, global_start=1)
    rich = RichUpgrTranscoder().decode(decoded, decode_context)
    assert len(rich.global_max_levels) == _NUM_UPGRADES
    assert rich.global_max_levels[UpgradeId.TERRAN_INFANTRY_ARMOR] == 2
    assert rich.global_start_levels[UpgradeId.TERRAN_INFANTRY_ARMOR] == 1


def test_it_decodes_player_uses_defaults_as_bool(decode_context):
    decoded = _make_decoded_upgr(player_defaults=1)
    rich = RichUpgrTranscoder().decode(decoded, decode_context)
    assert (
        rich.player_uses_defaults[PlayerId.PLAYER_1][UpgradeId.TERRAN_INFANTRY_ARMOR]
        is True
    )


def test_it_encodes_and_round_trips(decode_context, encode_context):
    decoded = _make_decoded_upgr()
    transcoder = RichUpgrTranscoder()
    rich = transcoder.decode(decoded, decode_context)
    re_decoded = transcoder.encode(rich, encode_context)
    assert re_decoded == decoded


def test_it_uses_encode_cache_for_same_object(decode_context, encode_context):
    decoded = _make_decoded_upgr()
    transcoder = RichUpgrTranscoder()
    rich = transcoder.decode(decoded, decode_context)
    result1 = transcoder.encode(rich, encode_context)
    result2 = transcoder.encode(rich, encode_context)
    assert result1 is result2
