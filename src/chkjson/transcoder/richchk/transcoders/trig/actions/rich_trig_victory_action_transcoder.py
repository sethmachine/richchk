"""Decode Victory trigger action."""

from chkjson.model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from chkjson.model.richchk.trig.actions.victory_action import VictoryAction

from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......util import logger
from ..rich_trigger_action_transcoder import RichTriggerActionTranscoder
from ..rich_trigger_action_transcoder_factory import (
    _RichTriggerActionRegistrableTranscoder,
)


class RichTriggerVictoryActionTranscoder(
    RichTriggerActionTranscoder[VictoryAction, DecodedTriggerAction],
    _RichTriggerActionRegistrableTranscoder,
    trigger_action_id=VictoryAction.action_id(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(RichTriggerVictoryActionTranscoder.__name__)

    def _decode(
        self,
        decoded_action: DecodedTriggerAction,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> VictoryAction:
        assert decoded_action.action_id == VictoryAction.action_id().id
        return VictoryAction()

    def _encode(
        self,
        rich_action: VictoryAction,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTriggerAction:
        return DecodedTriggerAction(
            _location_id=0,
            _text_string_id=0,
            _wav_string_id=0,
            _time=0,
            _first_group=0,
            _second_group=0,
            _action_argument_type=0,
            _action_id=rich_action.action_id().id,
            _quantifier_or_switch_or_order=0,
            _flags=0,
            _padding=0,
            _mask_flag=0,
        )
