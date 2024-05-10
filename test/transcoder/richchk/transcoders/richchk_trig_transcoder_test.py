import pytest

from chkjson.model.chk.trig.decoded_trig_section import DecodedTrigSection
from chkjson.model.richchk.mrgn.rich_mrgn_lookup import RichMrgnLookup
from chkjson.model.richchk.richchk_decode_context import RichChkDecodeContext
from chkjson.model.richchk.richchk_encode_context import RichChkEncodeContext
from chkjson.model.richchk.str.rich_str_lookup import RichStrLookup
from chkjson.transcoder.chk.transcoders.chk_trig_transcoder import ChkTrigTranscoder
from chkjson.transcoder.richchk.transcoders.richchk_trig_transcoder import (
    RichChkTrigTranscoder,
)

from ....chk_resources import DEMON_LORE_CHK_SECTION_FILE_PATHS


@pytest.fixture
def real_decoded_trig() -> DecodedTrigSection:
    with open(
        DEMON_LORE_CHK_SECTION_FILE_PATHS[DecodedTrigSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return ChkTrigTranscoder().decode(chk_binary_data)


def test_integration_it_decodes_and_encodes_back_to_chk_without_changing_data(
    real_decoded_trig,
):
    # these contexts won't work once string IDs are resolved to RichString
    # same with location IDs, CUWP IDs, and any other ID that gets de-referenced in the RichChk
    rich_chk_decode_context = RichChkDecodeContext(
        _rich_str_lookup=RichStrLookup(
            _string_by_id_lookup={},
            _id_by_string_lookup={},
        )
    )
    rich_chk_encode_context = RichChkEncodeContext(
        _rich_str_lookup=RichStrLookup(
            _string_by_id_lookup={},
            _id_by_string_lookup={},
        ),
        _rich_mrgn_lookup=RichMrgnLookup(
            _location_by_id_lookup={}, _id_by_location_lookup={}
        ),
    )
    rich_transcoder = RichChkTrigTranscoder()
    rich_trig = rich_transcoder.decode(
        real_decoded_trig,
        rich_chk_decode_context=rich_chk_decode_context,
    )
    decoded_trig_again = rich_transcoder.encode(rich_trig, rich_chk_encode_context)
    assert decoded_trig_again == real_decoded_trig
    assert (
        rich_transcoder.decode(decoded_trig_again, rich_chk_decode_context) == rich_trig
    )
