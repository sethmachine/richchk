import pytest

from richchk.model.chk.forc.decoded_forc_section import DecodedForcSection
from richchk.model.richchk.forc.force_flags import ForceFlags
from richchk.model.richchk.forc.rich_forc_section import RichForcSection
from richchk.model.richchk.forc.rich_force import RichForce
from richchk.model.richchk.richchk_decode_context import RichChkDecodeContext
from richchk.model.richchk.richchk_encode_context import RichChkEncodeContext
from richchk.model.richchk.str.rich_str_lookup import RichStrLookup
from richchk.model.richchk.str.rich_string import RichNullString, RichString
from richchk.transcoder.chk.transcoders.chk_forc_transcoder import ChkForcTranscoder
from richchk.transcoder.richchk.transcoders.rich_forc_transcoder import RichForcTranscoder

from ....chk_resources import CHK_SECTION_FILE_PATHS

_FORCE_0_NAME = "Alliance"
_FORCE_1_NAME = "Axis"

_STR_LOOKUP = RichStrLookup(
    _string_by_id_lookup={
        1: RichString(_value=_FORCE_0_NAME),
        2: RichString(_value=_FORCE_1_NAME),
    },
    _id_by_string_lookup={_FORCE_0_NAME: 1, _FORCE_1_NAME: 2},
)

_EXPECTED_PLAYER_FORCE_ASSIGNMENTS = [0, 0, 1, 1, 0, 0, 0, 0]
_EXPECTED_FORCE_FLAGS = ForceFlags(_random_start=False, _allies=True, _allied_victory=True, _shared_vision=False)


@pytest.fixture
def real_decoded_forc() -> DecodedForcSection:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedForcSection.section_name().value], "rb"
    ) as f:
        return ChkForcTranscoder().decode(f.read())


@pytest.fixture
def decode_context() -> RichChkDecodeContext:
    return RichChkDecodeContext(_rich_str_lookup=_STR_LOOKUP)


@pytest.fixture
def encode_context() -> RichChkEncodeContext:
    from richchk.model.richchk.mrgn.rich_mrgn_lookup import RichMrgnLookup
    from richchk.model.richchk.swnm.rich_swnm_lookup import RichSwnmLookup
    from richchk.model.richchk.uprp.rich_cuwp_lookup import RichCuwpLookup

    return RichChkEncodeContext(
        _rich_str_lookup=_STR_LOOKUP,
        _rich_mrgn_lookup=RichMrgnLookup(_location_by_id_lookup={}, _id_by_location_lookup={}),
        _rich_swnm_lookup=RichSwnmLookup(_switch_by_id_lookup={}, _id_by_switch_lookup={}),
        _rich_cuwp_lookup=RichCuwpLookup(_cuwp_by_id_lookup={}, _id_by_cuwp_lookup={}),
        _wav_metadata_lookup=None,
    )


def test_it_decodes_player_force_assignments(real_decoded_forc, decode_context):
    rich_forc = RichForcTranscoder().decode(real_decoded_forc, decode_context)
    assert rich_forc.player_force_assignments == _EXPECTED_PLAYER_FORCE_ASSIGNMENTS


def test_it_decodes_force_names(real_decoded_forc, decode_context):
    rich_forc = RichForcTranscoder().decode(real_decoded_forc, decode_context)
    assert rich_forc.forces[0].name == RichString(_value=_FORCE_0_NAME)
    assert rich_forc.forces[1].name == RichString(_value=_FORCE_1_NAME)
    assert isinstance(rich_forc.forces[2].name, RichNullString)
    assert isinstance(rich_forc.forces[3].name, RichNullString)


def test_it_decodes_force_flags(real_decoded_forc, decode_context):
    rich_forc = RichForcTranscoder().decode(real_decoded_forc, decode_context)
    assert rich_forc.forces[0].flags == _EXPECTED_FORCE_FLAGS
    assert rich_forc.forces[1].flags == _EXPECTED_FORCE_FLAGS
    assert rich_forc.forces[2].flags == ForceFlags()
    assert rich_forc.forces[3].flags == ForceFlags()


def test_it_decodes_and_encodes_without_changing_data(
    real_decoded_forc, decode_context, encode_context
):
    transcoder = RichForcTranscoder()
    rich_forc = transcoder.decode(real_decoded_forc, decode_context)
    re_decoded = transcoder.encode(rich_forc, encode_context)
    assert re_decoded == real_decoded_forc
