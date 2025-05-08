import pytest

from richchk.model.chk.ver.decoded_ver_section import DecodedVerSection
from richchk.model.richchk.mrgn.rich_mrgn_lookup import RichMrgnLookup
from richchk.model.richchk.richchk_decode_context import RichChkDecodeContext
from richchk.model.richchk.richchk_encode_context import RichChkEncodeContext
from richchk.model.richchk.str.rich_str_lookup import RichStrLookup
from richchk.model.richchk.swnm.rich_swnm_lookup import RichSwnmLookup
from richchk.model.richchk.uprp.rich_cuwp_lookup import RichCuwpLookup
from richchk.model.richchk.ver.ver_version import VerVersion
from richchk.transcoder.chk.transcoders.chk_ver_transcoder import ChkVerTranscoder
from richchk.transcoder.richchk.transcoders.rich_ver_transcoder import RichVerTranscoder

from ....chk_resources import CHK_SECTION_FILE_PATHS


@pytest.fixture
def real_decoded_ver() -> DecodedVerSection:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedVerSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return ChkVerTranscoder().decode(chk_binary_data)


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


def test_it_decodes_expected_version(real_decoded_ver, rich_decode_context):
    rich_ver = RichVerTranscoder().decode(
        real_decoded_ver,
        rich_chk_decode_context=rich_decode_context,
    )
    assert rich_ver.version == VerVersion.BROOD_WAR_100


def test_integration_it_decodes_and_encodes_back_without_changing_data(
    real_decoded_ver, rich_decode_context, rich_encode_context
):
    rich_ver = RichVerTranscoder().decode(
        real_decoded_ver,
        rich_chk_decode_context=rich_decode_context,
    )

    actual_decoded_ver = RichVerTranscoder().encode(
        rich_ver,
        rich_chk_encode_context=rich_encode_context,
    )
    rich_ver_again = RichVerTranscoder().decode(
        actual_decoded_ver,
        rich_chk_decode_context=rich_decode_context,
    )
    assert rich_ver == rich_ver_again
    # this assertion could fail because any non-semantic information
    # could be lost when decoding to a Rich representation
    assert actual_decoded_ver == real_decoded_ver
