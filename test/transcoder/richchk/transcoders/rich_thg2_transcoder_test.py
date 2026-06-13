import pytest

from richchk.model.chk.thg2.decoded_thg2_section import DecodedThg2Section
from richchk.model.richchk.mrgn.rich_mrgn_lookup import RichMrgnLookup
from richchk.model.richchk.richchk_decode_context import RichChkDecodeContext
from richchk.model.richchk.richchk_encode_context import RichChkEncodeContext
from richchk.model.richchk.str.rich_str_lookup import RichStrLookup
from richchk.model.richchk.swnm.rich_swnm_lookup import RichSwnmLookup
from richchk.model.richchk.uprp.rich_cuwp_lookup import RichCuwpLookup
from richchk.transcoder.chk.transcoders.chk_thg2_transcoder import ChkThg2Transcoder
from richchk.transcoder.richchk.transcoders.rich_thg2_transcoder import (
    RichThg2Transcoder,
)

from ....chk_resources import CHK_SECTION_FILE_PATHS


@pytest.fixture
def real_decoded_thg2() -> DecodedThg2Section:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedThg2Section.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return ChkThg2Transcoder().decode(chk_binary_data)


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


def test_it_decodes_empty_thg2_section(real_decoded_thg2, rich_decode_context):
    rich_thg2 = RichThg2Transcoder().decode(
        real_decoded_thg2,
        rich_chk_decode_context=rich_decode_context,
    )
    assert len(rich_thg2.entries) == 0


def test_integration_it_decodes_and_encodes_back_without_changing_data(
    real_decoded_thg2, rich_decode_context, rich_encode_context
):
    rich_thg2 = RichThg2Transcoder().decode(
        real_decoded_thg2,
        rich_chk_decode_context=rich_decode_context,
    )
    actual_decoded_thg2 = RichThg2Transcoder().encode(
        rich_thg2,
        rich_chk_encode_context=rich_encode_context,
    )
    rich_thg2_again = RichThg2Transcoder().decode(
        actual_decoded_thg2,
        rich_chk_decode_context=rich_decode_context,
    )
    assert rich_thg2 == rich_thg2_again
    assert actual_decoded_thg2 == real_decoded_thg2
