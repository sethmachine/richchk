from ......model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from ......model.richchk.mbrf.actions.text_message_briefing_action import (
    TextMessageBriefingAction,
)
from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......util import logger
from ..rich_briefing_action_transcoder import RichBriefingActionTranscoder
from ..rich_briefing_action_transcoder_factory import (
    _RichBriefingActionRegistrableTranscoder,
)


class TextMessageBriefingActionTranscoder(
    RichBriefingActionTranscoder[TextMessageBriefingAction, DecodedTriggerAction],
    _RichBriefingActionRegistrableTranscoder,
    briefing_action_id=TextMessageBriefingAction.action_id(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(TextMessageBriefingActionTranscoder.__name__)

    def _decode(
        self,
        decoded_action: DecodedTriggerAction,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> TextMessageBriefingAction:
        assert decoded_action.action_id == TextMessageBriefingAction.action_id().id
        return TextMessageBriefingAction(
            _text=rich_chk_decode_context.rich_str_lookup.get_string_by_id(
                decoded_action.text_string_id
            ),
            _duration_ms=decoded_action.time,
        )

    def _encode(
        self,
        rich_action: TextMessageBriefingAction,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTriggerAction:
        return DecodedTriggerAction(
            _location_id=0,
            _text_string_id=rich_chk_encode_context.rich_str_lookup.get_id_by_string(
                rich_action.message
            ),
            _wav_string_id=0,
            _time=rich_action.duration_ms,
            _first_group=0,
            _second_group=0,
            _action_argument_type=0,
            _action_id=rich_action.action_id().id,
            _quantifier_or_switch_or_order=0,
            _flags=0,
            _padding=0,
            _mask_flag=0,
        )
