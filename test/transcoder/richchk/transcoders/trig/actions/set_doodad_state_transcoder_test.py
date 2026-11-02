import pytest

from richchk.model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from richchk.model.richchk.mrgn.rich_location import RichLocation, RichNullLocation
from richchk.model.richchk.mrgn.rich_mrgn_lookup import RichMrgnLookup
from richchk.model.richchk.richchk_decode_context import RichChkDecodeContext
from richchk.model.richchk.richchk_encode_context import RichChkEncodeContext
from richchk.model.richchk.str.rich_str_lookup import RichStrLookup
from richchk.model.richchk.str.rich_string import RichString
from richchk.model.richchk.swnm.rich_swnm_lookup import RichSwnmLookup
from richchk.model.richchk.trig.actions.set_doodad_state_action import (
    SetDoodadStateAction,
)
from richchk.model.richchk.uprp.rich_cuwp_lookup import RichCuwpLookup
from richchk.transcoder.richchk.transcoders.trig.actions.set_doodad_state_transcoder import (
    RichTriggerSetDoodadStateTranscoder,
)


def _decoded_action(location_id: int) -> DecodedTriggerAction:
    return DecodedTriggerAction(
        _location_id=location_id,
        _text_string_id=0,
        _wav_string_id=0,
        _time=0,
        _first_group=0,
        _second_group=0,
        _action_argument_type=0,
        _action_id=SetDoodadStateAction.action_id().id,
        _quantifier_or_switch_or_order=4,
        _flags=0,
        _padding=0,
        _mask_flag=0,
    )


@pytest.fixture(scope="function")
def mrgn_lookup():
    used = RichLocation(1, 2, 3, 4, RichString(_value="used"), _index=5)
    return RichMrgnLookup(
        _location_by_id_lookup={5: used}, _id_by_location_lookup={used: 5}
    )


@pytest.fixture(scope="function")
def str_lookup():
    return RichStrLookup(_string_by_id_lookup={}, _id_by_string_lookup={})


@pytest.mark.parametrize("location_id", [0, 5, 14])
def test_it_round_trips_the_location_id(location_id, mrgn_lookup, str_lookup):
    decoded = _decoded_action(location_id)
    transcoder = RichTriggerSetDoodadStateTranscoder()
    rich = transcoder.decode(
        decoded,
        RichChkDecodeContext(
            _rich_str_lookup=str_lookup, _rich_mrgn_lookup=mrgn_lookup
        ),
    )
    assert isinstance(rich.location, RichNullLocation) == (location_id == 0)
    encoded = transcoder.encode(
        rich,
        RichChkEncodeContext(
            _rich_str_lookup=str_lookup,
            _rich_mrgn_lookup=mrgn_lookup,
            _rich_swnm_lookup=RichSwnmLookup(
                _switch_by_id_lookup={}, _id_by_switch_lookup={}
            ),
            _rich_cuwp_lookup=RichCuwpLookup(
                _cuwp_by_id_lookup={}, _id_by_cuwp_lookup={}
            ),
        ),
    )
    assert encoded.location_id == location_id
