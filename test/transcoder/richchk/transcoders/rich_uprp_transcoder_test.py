import pytest

from richchk.model.chk.uprp.decoded_uprp_section import DecodedUprpSection
from richchk.model.richchk.mrgn.rich_mrgn_lookup import RichMrgnLookup
from richchk.model.richchk.richchk_decode_context import RichChkDecodeContext
from richchk.model.richchk.richchk_encode_context import RichChkEncodeContext
from richchk.model.richchk.str.rich_str_lookup import RichStrLookup
from richchk.model.richchk.swnm.rich_swnm_lookup import RichSwnmLookup
from richchk.model.richchk.uprp.rich_cuwp_slot import (
    RichCuwpSlot,
    _RichCuwpSlotFlagsData,
)
from richchk.transcoder.chk.transcoders.chk_uprp_transcoder import ChkUprpTranscoder
from richchk.transcoder.richchk.transcoders.richchk_uprp_transcoder import (
    RichChkUprpTranscoder,
)

from ....chk_resources import CHK_SECTION_FILE_PATHS

# these are the expected CUWP based on triggers made in the map file
FIRST_EXPECTED_CUWP = RichCuwpSlot(
    _hitpoints_percentage=33,
    _shieldpoints_percentage=35,
    _energypoints_percentage=34,
    _resource_amount=0,
    _units_in_hangar=0,
    _cloaked=True,
    _burrowed=False,
    _building_in_transit=False,
    _hallucinated=True,
    _invincible=False,
    _flags_data=_RichCuwpSlotFlagsData(),
    _index=0,
)
SECOND_EXPECTED_CUWP = RichCuwpSlot(
    _hitpoints_percentage=25,
    _shieldpoints_percentage=50,
    _energypoints_percentage=30,
    _resource_amount=500,
    _units_in_hangar=8,
    _cloaked=True,
    _burrowed=True,
    _building_in_transit=False,
    _hallucinated=True,
    _invincible=True,
    _flags_data=_RichCuwpSlotFlagsData(),
    _index=1,
)


@pytest.fixture
def real_decoded_uprp() -> DecodedUprpSection:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedUprpSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return ChkUprpTranscoder().decode(chk_binary_data)


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
    )


def test_it_decodes_expected_cuwp_slots(
    real_decoded_uprp, rich_decode_context, rich_encode_context
):
    rich_uprp = RichChkUprpTranscoder().decode(
        real_decoded_uprp,
        rich_chk_decode_context=rich_decode_context,
    )
    assert FIRST_EXPECTED_CUWP == rich_uprp.cuwp_slots[0]
    assert SECOND_EXPECTED_CUWP == rich_uprp.cuwp_slots[1]


def test_integration_it_decodes_and_encodes_back_without_changing_data(
    real_decoded_uprp, rich_decode_context, rich_encode_context
):
    rich_uprp = RichChkUprpTranscoder().decode(
        real_decoded_uprp,
        rich_chk_decode_context=rich_decode_context,
    )

    actual_decoded_uprp = RichChkUprpTranscoder().encode(
        rich_uprp,
        rich_chk_encode_context=rich_encode_context,
    )
    rich_uprp_again = RichChkUprpTranscoder().decode(
        actual_decoded_uprp,
        rich_chk_decode_context=rich_decode_context,
    )
    assert rich_uprp == rich_uprp_again
    # this assertion could fail because any non-semantic information
    # could be lost when decoding to a Rich representation
    assert actual_decoded_uprp == real_decoded_uprp
