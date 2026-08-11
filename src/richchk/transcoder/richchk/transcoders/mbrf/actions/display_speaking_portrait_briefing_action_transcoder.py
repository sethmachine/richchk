from ......model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from ......model.richchk.mbrf.actions.display_speaking_portrait_briefing_action import (
    DisplaySpeakingPortraitBriefingAction,
)
from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......util import logger
from ..rich_briefing_action_transcoder import RichBriefingActionTranscoder
from ..rich_briefing_action_transcoder_factory import (
    _RichBriefingActionRegistrableTranscoder,
)


class DisplaySpeakingPortraitBriefingActionTranscoder(
    RichBriefingActionTranscoder[
        DisplaySpeakingPortraitBriefingAction, DecodedTriggerAction
    ],
    _RichBriefingActionRegistrableTranscoder,
    briefing_action_id=DisplaySpeakingPortraitBriefingAction.action_id(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(
            DisplaySpeakingPortraitBriefingActionTranscoder.__name__
        )

    def _decode(
        self,
        decoded_action: DecodedTriggerAction,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> DisplaySpeakingPortraitBriefingAction:
        assert (
            decoded_action.action_id
            == DisplaySpeakingPortraitBriefingAction.action_id().id
        )
        return DisplaySpeakingPortraitBriefingAction(
            _slot=decoded_action.second_group,
            _duration_ms=decoded_action.time,
        )

    def _encode(
        self,
        rich_action: DisplaySpeakingPortraitBriefingAction,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTriggerAction:
        return DecodedTriggerAction(
            _location_id=0,
            _text_string_id=0,
            _wav_string_id=0,
            _time=rich_action.duration_ms,
            _first_group=0,
            _second_group=rich_action.slot,
            _action_argument_type=0,
            _action_id=rich_action.action_id().id,
            _quantifier_or_switch_or_order=0,
            _flags=0,
            _padding=0,
            _mask_flag=0,
        )
