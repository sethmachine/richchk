import pytest

from richchk.io.richchk.lookups.mrgn.rich_mrgn_lookup_builder import (
    RichMrgnLookupBuilder,
)
from richchk.io.richchk.rich_str_lookup_builder import RichStrLookupBuilder
from richchk.model.chk.mrgn.decoded_mrgn_section import DecodedMrgnSection
from richchk.model.chk.str.decoded_str_section import DecodedStrSection
from richchk.model.chk.trig.decoded_trig_section import DecodedTrigSection
from richchk.model.richchk.mrgn.rich_mrgn_lookup import RichMrgnLookup
from richchk.model.richchk.richchk_decode_context import RichChkDecodeContext
from richchk.model.richchk.richchk_encode_context import RichChkEncodeContext
from richchk.model.richchk.str.rich_str_lookup import RichStrLookup
from richchk.transcoder.chk.transcoders.chk_mrgn_transcoder import ChkMrgnTranscoder
from richchk.transcoder.chk.transcoders.chk_str_transcoder import ChkStrTranscoder
from richchk.transcoder.chk.transcoders.chk_trig_transcoder import ChkTrigTranscoder
from richchk.transcoder.richchk.transcoders.richchk_mrgn_transcoder import (
    RichChkMrgnTranscoder,
)
from richchk.transcoder.richchk.transcoders.richchk_trig_transcoder import (
    RichChkTrigTranscoder,
)

from ....chk_resources import DEMON_LORE_CHK_SECTION_FILE_PATHS


@pytest.fixture(scope="function")
def real_decoded_trig() -> DecodedTrigSection:
    with open(
        DEMON_LORE_CHK_SECTION_FILE_PATHS[DecodedTrigSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return ChkTrigTranscoder().decode(chk_binary_data)


@pytest.fixture(scope="function")
def real_str_lookup() -> RichStrLookup:
    with open(
        DEMON_LORE_CHK_SECTION_FILE_PATHS[DecodedStrSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return RichStrLookupBuilder().build_lookup(
        decoded_str_section=ChkStrTranscoder().decode(chk_binary_data)
    )


@pytest.fixture(scope="function")
def real_mrgn_lookup(real_str_lookup) -> RichMrgnLookup:
    with open(
        DEMON_LORE_CHK_SECTION_FILE_PATHS[DecodedMrgnSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return RichMrgnLookupBuilder().build_lookup(
        RichChkMrgnTranscoder().decode(
            ChkMrgnTranscoder().decode(chk_binary_data),
            rich_chk_decode_context=RichChkDecodeContext(
                _rich_str_lookup=real_str_lookup, _rich_mrgn_lookup=None
            ),
        )
    )


@pytest.fixture(scope="function")
def real_rich_chk_decode_context(real_str_lookup, real_mrgn_lookup):
    return RichChkDecodeContext(
        _rich_str_lookup=real_str_lookup, _rich_mrgn_lookup=real_mrgn_lookup
    )


@pytest.fixture(scope="function")
def real_rich_chk_encode_context(real_str_lookup, real_mrgn_lookup):
    return RichChkEncodeContext(
        _rich_str_lookup=real_str_lookup, _rich_mrgn_lookup=real_mrgn_lookup
    )


def test_integration_it_decodes_and_encodes_back_to_chk_without_changing_data(
    real_decoded_trig, real_rich_chk_decode_context, real_rich_chk_encode_context
):
    rich_transcoder = RichChkTrigTranscoder()
    rich_trig = rich_transcoder.decode(
        real_decoded_trig,
        rich_chk_decode_context=real_rich_chk_decode_context,
    )
    decoded_trig_again = rich_transcoder.encode(rich_trig, real_rich_chk_encode_context)
    assert decoded_trig_again == real_decoded_trig
    rich_trig_again = rich_transcoder.decode(
        decoded_trig_again, real_rich_chk_decode_context
    )
    assert rich_trig_again == rich_trig
