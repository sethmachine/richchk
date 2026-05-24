import pytest

from richchk.model.chk.side.decoded_side_section import DecodedSideSection
from richchk.model.richchk.richchk_decode_context import RichChkDecodeContext
from richchk.model.richchk.richchk_encode_context import RichChkEncodeContext
from richchk.model.richchk.side.player_race import PlayerRace
from richchk.model.richchk.side.rich_side_section import RichSideSection
from richchk.model.richchk.str.rich_str_lookup import RichStrLookup
from richchk.transcoder.chk.transcoders.chk_side_transcoder import ChkSideTranscoder
from richchk.transcoder.richchk.transcoders.rich_side_transcoder import (
    RichSideTranscoder,
)

from ....chk_resources import CHK_SECTION_FILE_PATHS

_NUM_PLAYERS = 12

_EXPECTED_RACES = [
    PlayerRace.TERRAN,
    PlayerRace.ZERG,
    PlayerRace.PROTOSS,
    PlayerRace.RANDOM,
    PlayerRace.INACTIVE,
    PlayerRace.INACTIVE,
    PlayerRace.INACTIVE,
    PlayerRace.INACTIVE,
    PlayerRace.INACTIVE,
    PlayerRace.INACTIVE,
    PlayerRace.INACTIVE,
    PlayerRace.INACTIVE,
]

_EMPTY_STR_LOOKUP = RichStrLookup(_string_by_id_lookup={}, _id_by_string_lookup={})


@pytest.fixture
def real_decoded_side() -> DecodedSideSection:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedSideSection.section_name().value], "rb"
    ) as f:
        return ChkSideTranscoder().decode(f.read())


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


def test_it_decodes_expected_player_races(real_decoded_side, decode_context):
    rich_side = RichSideTranscoder().decode(real_decoded_side, decode_context)
    assert rich_side.player_races == _EXPECTED_RACES


def test_it_encodes_player_races(encode_context):
    rich_side = RichSideSection(_player_races=_EXPECTED_RACES)
    decoded = RichSideTranscoder().encode(rich_side, encode_context)
    assert decoded.player_races == [race.id for race in _EXPECTED_RACES]


def test_it_decodes_and_encodes_without_changing_data(
    real_decoded_side, decode_context, encode_context
):
    transcoder = RichSideTranscoder()
    rich_side = transcoder.decode(real_decoded_side, decode_context)
    re_decoded = transcoder.encode(rich_side, encode_context)
    assert re_decoded == real_decoded_side
