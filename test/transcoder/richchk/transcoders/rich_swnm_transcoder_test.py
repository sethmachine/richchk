import pytest

from richchk.model.chk.swnm.decoded_swnm_section import DecodedSwnmSection
from richchk.model.richchk.mrgn.rich_mrgn_lookup import RichMrgnLookup
from richchk.model.richchk.richchk_decode_context import RichChkDecodeContext
from richchk.model.richchk.richchk_encode_context import RichChkEncodeContext
from richchk.model.richchk.str.rich_str_lookup import RichStrLookup
from richchk.model.richchk.str.rich_string import RichString
from richchk.model.richchk.swnm.rich_switch import RichSwitch
from richchk.model.richchk.swnm.rich_swnm_lookup import RichSwnmLookup
from richchk.model.richchk.swnm.rich_swnm_section import RichSwnmSection
from richchk.model.richchk.uprp.rich_cuwp_lookup import RichCuwpLookup
from richchk.transcoder.chk.transcoders.chk_swnm_transcoder import ChkSwnmTranscoder
from richchk.transcoder.richchk.transcoders.rich_swnm_transcoder import (
    RichChkSwnmTranscoder,
)

from ....chk_resources import CHK_SECTION_FILE_PATHS

_NUM_SWITCHES = 256


@pytest.fixture
def real_decoded_swnm() -> DecodedSwnmSection:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedSwnmSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return ChkSwnmTranscoder().decode(chk_binary_data)


@pytest.fixture
def real_rich_chk_decode_context(real_decoded_swnm) -> RichChkDecodeContext:
    # the lookups are based on the real Switch names data in the CHK
    switch_by_id = {switch_id: RichSwitch() for switch_id in range(0, _NUM_SWITCHES)}
    switch_by_id[3] = RichSwitch(RichString(_value="FLOOF"), _index=3)
    switch_by_id[4] = RichSwitch(RichString(_value="Switch 5"), _index=4)
    switch_by_id[6] = RichSwitch(RichString(_value="Switch 7 Renamed"), _index=6)
    return RichChkDecodeContext(
        _rich_str_lookup=RichStrLookup(
            _string_by_id_lookup={
                16: RichString(_value="FLOOF"),
                15: RichString(_value="Switch 5"),
                14: RichString(_value="Switch 7 Renamed"),
            },
            _id_by_string_lookup={"FLOOF": 16, "Switch 5": 15, "Switch 7 Renamed": 14},
        ),
        _rich_mrgn_lookup=RichMrgnLookup(
            _location_by_id_lookup={}, _id_by_location_lookup={}
        ),
        _rich_swnm_lookup=RichSwnmLookup(
            _switch_by_id_lookup=switch_by_id, _id_by_switch_lookup={}
        ),
    )


@pytest.fixture
def real_rich_chk_encode_context(real_decoded_swnm) -> RichChkEncodeContext:
    # the lookups are based on the real Switch names data in the CHK
    return RichChkEncodeContext(
        _rich_str_lookup=RichStrLookup(
            _string_by_id_lookup={
                16: RichString(_value="FLOOF"),
                15: RichString(_value="Switch 5"),
                14: RichString(_value="Switch 7 Renamed"),
            },
            _id_by_string_lookup={"FLOOF": 16, "Switch 5": 15, "Switch 7 Renamed": 14},
        ),
        _rich_mrgn_lookup=RichMrgnLookup(
            _location_by_id_lookup={}, _id_by_location_lookup={}
        ),
        _rich_swnm_lookup=RichSwnmLookup(
            _switch_by_id_lookup={}, _id_by_switch_lookup={}
        ),
        _rich_cuwp_lookup=RichCuwpLookup(_cuwp_by_id_lookup={}, _id_by_cuwp_lookup={}),
        _wav_metadata_lookup=None,
    )


def test_integration_it_decodes_all_switch_names(
    real_decoded_swnm, real_rich_chk_decode_context
):
    rich_transcoder = RichChkSwnmTranscoder()
    rich_swnm = rich_transcoder.decode(
        real_decoded_swnm, rich_chk_decode_context=real_rich_chk_decode_context
    )
    for switch in rich_swnm.switches:
        if switch.index:
            maybe_switch = (
                real_rich_chk_decode_context.rich_swnm_lookup.get_switch_by_id(
                    switch.index
                )
            )
            assert maybe_switch is not None
            assert maybe_switch == switch


def test_it_encodes_all_switch_names():
    rich_transcoder = RichChkSwnmTranscoder()
    switches = [RichSwitch() for x in range(0, _NUM_SWITCHES)]
    switches[0] = RichSwitch(
        _custom_name=RichString(_value="custom name for switch 1"), _index=1
    )
    rich_swnm = RichSwnmSection(_switches=switches)
    decoded_swnm = rich_transcoder.encode(
        rich_swnm,
        rich_chk_encode_context=RichChkEncodeContext(
            _rich_str_lookup=RichStrLookup(
                _string_by_id_lookup={},
                _id_by_string_lookup={switches[0].custom_name.value: 5},
            ),
            _rich_mrgn_lookup=RichMrgnLookup(
                _location_by_id_lookup={}, _id_by_location_lookup={}
            ),
            _rich_swnm_lookup=RichSwnmLookup(
                _switch_by_id_lookup={}, _id_by_switch_lookup={}
            ),
            _rich_cuwp_lookup=RichCuwpLookup(
                _cuwp_by_id_lookup={}, _id_by_cuwp_lookup={}
            ),
            _wav_metadata_lookup=None,
        ),
    )
    assert decoded_swnm.switch_string_ids[0] == 5
    assert all([string_id == 0 for string_id in decoded_swnm.switch_string_ids[1:]])


def test_integration_it_decodes_and_encodes_without_changing_data(
    real_decoded_swnm, real_rich_chk_decode_context, real_rich_chk_encode_context
):
    rich_transcoder = RichChkSwnmTranscoder()
    rich_swnm = rich_transcoder.decode(
        real_decoded_swnm, rich_chk_decode_context=real_rich_chk_decode_context
    )
    actual_decoded_swnm = rich_transcoder.encode(
        rich_swnm, real_rich_chk_encode_context
    )
    assert actual_decoded_swnm == real_decoded_swnm
    assert rich_swnm == rich_transcoder.decode(
        actual_decoded_swnm, rich_chk_decode_context=real_rich_chk_decode_context
    )
