import pytest

from richchk.io.richchk.rich_str_lookup_builder import RichStrLookupBuilder
from richchk.model.chk.mbrf.decoded_mbrf_section import DecodedMbrfSection
from richchk.model.chk.str.decoded_str_section import DecodedStrSection
from richchk.model.richchk.mbrf.actions.wait_briefing_action import WaitBriefingAction
from richchk.model.richchk.mbrf.briefing_action_id import BriefingActionId
from richchk.model.richchk.mbrf.rich_briefing import RichBriefing
from richchk.model.richchk.mbrf.rich_mbrf_section import RichMbrfSection
from richchk.model.richchk.mrgn.rich_mrgn_lookup import RichMrgnLookup
from richchk.model.richchk.richchk_decode_context import RichChkDecodeContext
from richchk.model.richchk.richchk_encode_context import RichChkEncodeContext
from richchk.model.richchk.str.rich_str_lookup import RichStrLookup
from richchk.model.richchk.swnm.rich_swnm_lookup import RichSwnmLookup
from richchk.model.richchk.trig.player_id import PlayerId
from richchk.model.richchk.uprp.rich_cuwp_lookup import RichCuwpLookup
from richchk.transcoder.chk.transcoders.chk_mbrf_transcoder import ChkMbrfTranscoder
from richchk.transcoder.chk.transcoders.chk_str_transcoder import ChkStrTranscoder
from richchk.transcoder.richchk.transcoders.richchk_mbrf_transcoder import (
    RichChkMbrfTranscoder,
)

from ....chk_resources import CHK_SECTION_FILE_PATHS

_MBRF_SECTION_KEY = DecodedMbrfSection.section_name().value
_WAIT_ACTION_TIME_MS = 555


@pytest.fixture(scope="function")
def real_decoded_mbrf() -> DecodedMbrfSection:
    with open(CHK_SECTION_FILE_PATHS[_MBRF_SECTION_KEY], "rb") as f:
        return ChkMbrfTranscoder().decode(f.read())


@pytest.fixture(scope="function")
def real_str_lookup() -> RichStrLookup:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedStrSection.section_name().value], "rb"
    ) as f:
        return RichStrLookupBuilder().build_lookup(
            decoded_string_section=ChkStrTranscoder().decode(f.read())
        )


@pytest.fixture(scope="function")
def decode_context(real_str_lookup: RichStrLookup) -> RichChkDecodeContext:
    return RichChkDecodeContext(_rich_str_lookup=real_str_lookup)


@pytest.fixture(scope="function")
def encode_context(real_str_lookup: RichStrLookup) -> RichChkEncodeContext:
    return RichChkEncodeContext(
        _rich_str_lookup=real_str_lookup,
        _rich_mrgn_lookup=RichMrgnLookup(
            _location_by_id_lookup={}, _id_by_location_lookup={}
        ),
        _rich_swnm_lookup=RichSwnmLookup(
            _switch_by_id_lookup={}, _id_by_switch_lookup={}
        ),
        _rich_cuwp_lookup=RichCuwpLookup(_cuwp_by_id_lookup={}, _id_by_cuwp_lookup={}),
    )


def test_it_decodes_one_briefing(
    real_decoded_mbrf: DecodedMbrfSection, decode_context: RichChkDecodeContext
):
    transcoder = RichChkMbrfTranscoder()
    rich_mbrf = transcoder.decode(real_decoded_mbrf, decode_context)
    assert isinstance(rich_mbrf, RichMbrfSection)
    assert len(rich_mbrf.briefings) == 1


def test_it_decodes_wait_action(
    real_decoded_mbrf: DecodedMbrfSection, decode_context: RichChkDecodeContext
):
    transcoder = RichChkMbrfTranscoder()
    rich_mbrf = transcoder.decode(real_decoded_mbrf, decode_context)
    briefing = rich_mbrf.briefings[0]
    assert len(briefing.actions) == 1
    action = briefing.actions[0]
    assert isinstance(action, WaitBriefingAction)
    assert action.action_id() == BriefingActionId.WAIT
    assert action.milliseconds == _WAIT_ACTION_TIME_MS


def test_it_decodes_player_execution(
    real_decoded_mbrf: DecodedMbrfSection, decode_context: RichChkDecodeContext
):
    transcoder = RichChkMbrfTranscoder()
    rich_mbrf = transcoder.decode(real_decoded_mbrf, decode_context)
    briefing = rich_mbrf.briefings[0]
    assert PlayerId.PLAYER_3 in briefing.players


def test_round_trip_decode_encode_preserves_briefings(
    real_decoded_mbrf: DecodedMbrfSection,
    decode_context: RichChkDecodeContext,
    encode_context: RichChkEncodeContext,
):
    transcoder = RichChkMbrfTranscoder()
    rich_mbrf = transcoder.decode(real_decoded_mbrf, decode_context)
    re_encoded = transcoder.encode(rich_mbrf, encode_context)
    assert re_encoded == real_decoded_mbrf


def test_it_encodes_new_briefing_with_wait_action(
    encode_context: RichChkEncodeContext,
):
    transcoder = RichChkMbrfTranscoder()
    briefing = RichBriefing(
        _actions=[WaitBriefingAction(_milliseconds=1000)],
        _players={PlayerId.PLAYER_1},
    )
    rich_mbrf = RichMbrfSection(_briefings=[briefing])
    encoded = transcoder.encode(rich_mbrf, encode_context)
    assert len(encoded.triggers) == 1
    decode_ctx = RichChkDecodeContext(_rich_str_lookup=encode_context.rich_str_lookup)
    decoded_again = transcoder.decode(encoded, decode_ctx)
    assert len(decoded_again.briefings) == 1
    action = decoded_again.briefings[0].actions[0]
    assert isinstance(action, WaitBriefingAction)
    assert action.milliseconds == 1000
