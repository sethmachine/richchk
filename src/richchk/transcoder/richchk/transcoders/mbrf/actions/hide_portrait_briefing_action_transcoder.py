from ......model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from ......model.richchk.mbrf.actions.hide_portrait_briefing_action import (
    HidePortraitBriefingAction,
)
from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......util import logger
from ..rich_briefing_action_transcoder import RichBriefingActionTranscoder
from ..rich_briefing_action_transcoder_factory import (
    _RichBriefingActionRegistrableTranscoder,
)


class HidePortraitBriefingActionTranscoder(
    RichBriefingActionTranscoder[HidePortraitBriefingAction, DecodedTriggerAction],
    _RichBriefingActionRegistrableTranscoder,
    briefing_action_id=HidePortraitBriefingAction.action_id(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(HidePortraitBriefingActionTranscoder.__name__)

    def _decode(
        self,
        decoded_action: DecodedTriggerAction,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> HidePortraitBriefingAction:
        assert decoded_action.action_id == HidePortraitBriefingAction.action_id().id
        return HidePortraitBriefingAction(_slot=decoded_action.second_group)

    def _encode(
        self,
        rich_action: HidePortraitBriefingAction,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTriggerAction:
        return DecodedTriggerAction(
            _location_id=0,
            _text_string_id=0,
            _wav_string_id=0,
            _time=0,
            _first_group=0,
            _second_group=rich_action.slot,
            _action_argument_type=0,
            _action_id=rich_action.action_id().id,
            _quantifier_or_switch_or_order=0,
            _flags=0,
            _padding=0,
            _mask_flag=0,
        )
