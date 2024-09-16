"""Decode Set Countdown Timer trigger action."""

from ......model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......model.richchk.trig.actions.set_countdown_timer import SetCountdownTimerAction
from ......model.richchk.trig.enums.amount_modifier import AmountModifier
from ......util import logger
from ...helpers.richchk_enum_transcoder import RichChkEnumTranscoder
from ..rich_trigger_action_transcoder import RichTriggerActionTranscoder
from ..rich_trigger_action_transcoder_factory import (
    _RichTriggerActionRegistrableTranscoder,
)


class RichTriggerSetCountdownTimerActionTranscoder(
    RichTriggerActionTranscoder[SetCountdownTimerAction, DecodedTriggerAction],
    _RichTriggerActionRegistrableTranscoder,
    trigger_action_id=SetCountdownTimerAction.action_id(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(
            RichTriggerSetCountdownTimerActionTranscoder.__name__
        )

    def _decode(
        self,
        decoded_action: DecodedTriggerAction,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> SetCountdownTimerAction:
        assert decoded_action.action_id == SetCountdownTimerAction.action_id().id
        return SetCountdownTimerAction(
            _seconds=decoded_action.time,
            _amount_modifier=RichChkEnumTranscoder.decode_enum(
                decoded_action.quantifier_or_switch_or_order, AmountModifier
            ),
        )

    def _encode(
        self,
        rich_action: SetCountdownTimerAction,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTriggerAction:
        return DecodedTriggerAction(
            _location_id=0,
            _text_string_id=0,
            _wav_string_id=0,
            _time=rich_action.seconds,
            _first_group=0,
            _second_group=0,
            _action_argument_type=0,
            _action_id=rich_action.action_id().id,
            _quantifier_or_switch_or_order=RichChkEnumTranscoder.encode_enum(
                rich_action.amount_modifier
            ),
            _flags=0,
            _padding=0,
            _mask_flag=0,
        )
