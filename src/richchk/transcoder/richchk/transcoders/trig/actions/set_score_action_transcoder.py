"""Set score action."""

from ......model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......model.richchk.trig.actions.set_score_action import SetScoreAction
from ......model.richchk.trig.enums.amount_modifier import AmountModifier
from ......model.richchk.trig.enums.score_type import ScoreType
from ......model.richchk.trig.player_id import PlayerId
from ......util import logger
from ...helpers.richchk_enum_transcoder import RichChkEnumTranscoder
from ..rich_trigger_action_transcoder import RichTriggerActionTranscoder
from ..rich_trigger_action_transcoder_factory import (
    _RichTriggerActionRegistrableTranscoder,
)


class RichTriggerSetScoreActionTranscoder(
    RichTriggerActionTranscoder[SetScoreAction, DecodedTriggerAction],
    _RichTriggerActionRegistrableTranscoder,
    trigger_action_id=SetScoreAction.action_id(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(RichTriggerSetScoreActionTranscoder.__name__)

    def _decode(
        self,
        decoded_action: DecodedTriggerAction,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> SetScoreAction:
        assert decoded_action.action_id == SetScoreAction.action_id().id
        return SetScoreAction(
            _group=RichChkEnumTranscoder.decode_enum(
                decoded_action.first_group, PlayerId
            ),
            _amount_modifier=RichChkEnumTranscoder.decode_enum(
                decoded_action.quantifier_or_switch_or_order, AmountModifier
            ),
            _amount=decoded_action.second_group,
            _score_type=RichChkEnumTranscoder.decode_enum(
                decoded_action.action_argument_type, ScoreType
            ),
        )

    def _encode(
        self,
        rich_action: SetScoreAction,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTriggerAction:
        return DecodedTriggerAction(
            _location_id=0,
            _text_string_id=0,
            _wav_string_id=0,
            _time=0,
            _first_group=RichChkEnumTranscoder.encode_enum(rich_action.group),
            _second_group=rich_action.amount,
            _action_argument_type=RichChkEnumTranscoder.encode_enum(
                rich_action.score_type
            ),
            _action_id=rich_action.action_id().id,
            _quantifier_or_switch_or_order=RichChkEnumTranscoder.encode_enum(
                rich_action.amount_modifier
            ),
            _flags=0,
            _padding=0,
            _mask_flag=0,
        )
