import pytest

from richchk.io.richchk.rich_str_lookup_builder import RichStrLookupBuilder
from richchk.model.chk.sprp.decoded_sprp_section import DecodedSprpSection
from richchk.model.chk.str.decoded_str_section import DecodedStrSection
from richchk.model.richchk.mrgn.rich_mrgn_lookup import RichMrgnLookup
from richchk.model.richchk.richchk_decode_context import RichChkDecodeContext
from richchk.model.richchk.richchk_encode_context import RichChkEncodeContext
from richchk.model.richchk.sprp.rich_sprp_section import RichSprpSection
from richchk.model.richchk.str.rich_str_lookup import RichStrLookup
from richchk.model.richchk.swnm.rich_swnm_lookup import RichSwnmLookup
from richchk.model.richchk.uprp.rich_cuwp_lookup import RichCuwpLookup
from richchk.transcoder.chk.transcoders.chk_sprp_transcoder import ChkSprpTranscoder
from richchk.transcoder.chk.transcoders.chk_str_transcoder import ChkStrTranscoder
from richchk.transcoder.richchk.transcoders.richchk_sprp_transcoder import (
    RichSprpTranscoder,
)

from ....chk_resources import CHK_SECTION_FILE_PATHS

_SPRP_SECTION_KEY = DecodedSprpSection.section_name().value
_EXPECTED_SCENARIO_NAME = "Untitled Scenario"
_EXPECTED_SCENARIO_DESCRIPTION = "Destroy all enemy buildings."


@pytest.fixture(scope="function")
def real_decoded_sprp() -> DecodedSprpSection:
    with open(CHK_SECTION_FILE_PATHS[_SPRP_SECTION_KEY], "rb") as f:
        return ChkSprpTranscoder().decode(f.read())


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


def test_it_decodes_scenario_name(
    real_decoded_sprp: DecodedSprpSection, decode_context: RichChkDecodeContext
):
    rich_sprp = RichSprpTranscoder().decode(real_decoded_sprp, decode_context)
    assert isinstance(rich_sprp, RichSprpSection)
    assert rich_sprp.scenario_name.value == _EXPECTED_SCENARIO_NAME


def test_it_decodes_scenario_description(
    real_decoded_sprp: DecodedSprpSection, decode_context: RichChkDecodeContext
):
    rich_sprp = RichSprpTranscoder().decode(real_decoded_sprp, decode_context)
    assert rich_sprp.scenario_description.value == _EXPECTED_SCENARIO_DESCRIPTION


def test_round_trip_decode_encode_preserves_data(
    real_decoded_sprp: DecodedSprpSection,
    decode_context: RichChkDecodeContext,
    encode_context: RichChkEncodeContext,
):
    transcoder = RichSprpTranscoder()
    rich_sprp = transcoder.decode(real_decoded_sprp, decode_context)
    re_encoded = transcoder.encode(rich_sprp, encode_context)
    assert re_encoded == real_decoded_sprp
