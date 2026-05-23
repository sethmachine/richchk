import pytest

from richchk.model.chk.ownr.decoded_ownr_section import DecodedOwnrSection
from richchk.model.richchk.ownr.player_controller import PlayerController
from richchk.model.richchk.ownr.rich_ownr_section import RichOwnrSection
from richchk.model.richchk.richchk_decode_context import RichChkDecodeContext
from richchk.model.richchk.richchk_encode_context import RichChkEncodeContext
from richchk.model.richchk.str.rich_str_lookup import RichStrLookup
from richchk.transcoder.chk.transcoders.chk_ownr_transcoder import ChkOwnrTranscoder
from richchk.transcoder.richchk.transcoders.rich_ownr_transcoder import RichOwnrTranscoder

from ....chk_resources import CHK_SECTION_FILE_PATHS

_NUM_PLAYERS = 12

_EXPECTED_CONTROLLERS = [
    PlayerController.HUMAN,
    PlayerController.COMPUTER,
    PlayerController.RESCUE_PASSIVE,
    PlayerController.NEUTRAL,
    PlayerController.INACTIVE,
    PlayerController.INACTIVE,
    PlayerController.INACTIVE,
    PlayerController.INACTIVE,
    PlayerController.INACTIVE,
    PlayerController.INACTIVE,
    PlayerController.INACTIVE,
    PlayerController.INACTIVE,
]

_EMPTY_STR_LOOKUP = RichStrLookup(
    _string_by_id_lookup={}, _id_by_string_lookup={}
)


@pytest.fixture
def real_decoded_ownr() -> DecodedOwnrSection:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedOwnrSection.section_name().value], "rb"
    ) as f:
        return ChkOwnrTranscoder().decode(f.read())


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
        _rich_mrgn_lookup=RichMrgnLookup(_location_by_id_lookup={}, _id_by_location_lookup={}),
        _rich_swnm_lookup=RichSwnmLookup(_switch_by_id_lookup={}, _id_by_switch_lookup={}),
        _rich_cuwp_lookup=RichCuwpLookup(_cuwp_by_id_lookup={}, _id_by_cuwp_lookup={}),
        _wav_metadata_lookup=None,
    )


def test_it_decodes_expected_player_controllers(real_decoded_ownr, decode_context):
    rich_ownr = RichOwnrTranscoder().decode(real_decoded_ownr, decode_context)
    assert rich_ownr.player_controllers == _EXPECTED_CONTROLLERS


def test_it_encodes_player_controllers(encode_context):
    rich_ownr = RichOwnrSection(_player_controllers=_EXPECTED_CONTROLLERS)
    decoded = RichOwnrTranscoder().encode(rich_ownr, encode_context)
    assert decoded.player_controllers == [
        PlayerController.HUMAN.id,
        PlayerController.COMPUTER.id,
        PlayerController.RESCUE_PASSIVE.id,
        PlayerController.NEUTRAL.id,
        PlayerController.INACTIVE.id,
        PlayerController.INACTIVE.id,
        PlayerController.INACTIVE.id,
        PlayerController.INACTIVE.id,
        PlayerController.INACTIVE.id,
        PlayerController.INACTIVE.id,
        PlayerController.INACTIVE.id,
        PlayerController.INACTIVE.id,
    ]


def test_it_decodes_and_encodes_without_changing_data(
    real_decoded_ownr, decode_context, encode_context
):
    transcoder = RichOwnrTranscoder()
    rich_ownr = transcoder.decode(real_decoded_ownr, decode_context)
    re_decoded = transcoder.encode(rich_ownr, encode_context)
    assert re_decoded == real_decoded_ownr
