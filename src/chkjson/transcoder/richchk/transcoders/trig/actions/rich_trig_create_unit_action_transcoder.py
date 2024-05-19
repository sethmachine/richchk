"""Decode Victory trigger action."""

from chkjson.model.chk.trig.decoded_trigger_action import DecodedTriggerAction

from ......model.richchk.mrgn.rich_location import RichLocation
from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......model.richchk.trig.actions.create_unit_action import CreateUnitAction
from ......model.richchk.trig.player_id import PlayerId
from ......model.richchk.unis.unit_id import UnitId
from ......util import logger
from ...helpers.richchk_enum_transcoder import RichChkEnumTranscoder
from ..rich_trigger_action_transcoder import RichTriggerActionTranscoder
from ..rich_trigger_action_transcoder_factory import (
    _RichTriggerActionRegistrableTranscoder,
)


class RichTriggerVictoryActionTranscoder(
    RichTriggerActionTranscoder[CreateUnitAction, DecodedTriggerAction],
    _RichTriggerActionRegistrableTranscoder,
    trigger_action_id=CreateUnitAction.action_id(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(RichTriggerVictoryActionTranscoder.__name__)

    def decode(
        self,
        decoded_action: DecodedTriggerAction,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> CreateUnitAction:
        assert decoded_action.action_id == CreateUnitAction.action_id().id
        assert rich_chk_decode_context.rich_mrgn_lookup is not None
        maybe_location = rich_chk_decode_context.rich_mrgn_lookup.get_location_by_id(
            decoded_action.location_id
        )
        assert isinstance(maybe_location, RichLocation)
        return CreateUnitAction(
            for_player=RichChkEnumTranscoder.decode_enum(
                decoded_action.first_group, PlayerId
            ),
            amount=decoded_action.quantifier_or_switch_or_order,
            unit_id=RichChkEnumTranscoder.decode_enum(
                decoded_action.action_argument_type, UnitId
            ),
            location=maybe_location,
        )

    def encode(
        self,
        rich_action: CreateUnitAction,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTriggerAction:
        assert rich_chk_encode_context.rich_mrgn_lookup is not None
        maybe_location_id = rich_chk_encode_context.rich_mrgn_lookup.get_id_by_location(
            rich_action.location
        )
        assert maybe_location_id is not None
        return DecodedTriggerAction(
            _location_id=maybe_location_id,
            _text_string_id=0,
            _wav_string_id=0,
            _time=0,
            _first_group=rich_action.for_player.id,
            _second_group=0,
            _action_argument_type=rich_action.unit_id.id,
            _action_id=CreateUnitAction.action_id().id,
            _quantifier_or_switch_or_order=rich_action.amount,
            _flags=0,
            _padding=0,
            _mask_flag=0,
        )
