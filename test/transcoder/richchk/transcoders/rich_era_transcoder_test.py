import pytest

from richchk.model.chk.era.decoded_era_section import DecodedEraSection
from richchk.model.richchk.era.tileset import StarCraftTileset
from richchk.model.richchk.mrgn.rich_mrgn_lookup import RichMrgnLookup
from richchk.model.richchk.richchk_decode_context import RichChkDecodeContext
from richchk.model.richchk.richchk_encode_context import RichChkEncodeContext
from richchk.model.richchk.str.rich_str_lookup import RichStrLookup
from richchk.model.richchk.swnm.rich_swnm_lookup import RichSwnmLookup
from richchk.model.richchk.uprp.rich_cuwp_lookup import RichCuwpLookup
from richchk.transcoder.chk.transcoders.chk_era_transcoder import ChkEraTranscoder
from richchk.transcoder.richchk.transcoders.rich_era_transcoder import RichEraTranscoder

from ....chk_resources import CHK_SECTION_FILE_PATHS


@pytest.fixture
def real_decoded_era() -> DecodedEraSection:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedEraSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return ChkEraTranscoder().decode(chk_binary_data)


@pytest.fixture
def rich_decode_context():
    return RichChkDecodeContext(
        _rich_str_lookup=RichStrLookup(
            _string_by_id_lookup={},
            _id_by_string_lookup={},
        )
    )


@pytest.fixture
def rich_encode_context():
    return RichChkEncodeContext(
        _rich_str_lookup=RichStrLookup(
            _string_by_id_lookup={}, _id_by_string_lookup={}
        ),
        _rich_mrgn_lookup=RichMrgnLookup(
            _location_by_id_lookup={}, _id_by_location_lookup={}
        ),
        _rich_swnm_lookup=RichSwnmLookup(
            _switch_by_id_lookup={}, _id_by_switch_lookup={}
        ),
        _rich_cuwp_lookup=RichCuwpLookup(_cuwp_by_id_lookup={}, _id_by_cuwp_lookup={}),
    )


def test_it_decodes_expected_tileset(real_decoded_era, rich_decode_context):
    rich_era = RichEraTranscoder().decode(
        real_decoded_era,
        rich_chk_decode_context=rich_decode_context,
    )
    assert rich_era.tileset == StarCraftTileset.JUNGLE


def test_integration_it_decodes_and_encodes_back_without_changing_data(
    real_decoded_era, rich_decode_context, rich_encode_context
):
    rich_era = RichEraTranscoder().decode(
        real_decoded_era,
        rich_chk_decode_context=rich_decode_context,
    )
    actual_decoded_era = RichEraTranscoder().encode(
        rich_era,
        rich_chk_encode_context=rich_encode_context,
    )
    rich_era_again = RichEraTranscoder().decode(
        actual_decoded_era,
        rich_chk_decode_context=rich_decode_context,
    )
    assert rich_era == rich_era_again
    assert actual_decoded_era == real_decoded_era
