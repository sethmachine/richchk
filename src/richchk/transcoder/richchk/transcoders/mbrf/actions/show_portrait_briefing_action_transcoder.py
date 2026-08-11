from ......model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from ......model.richchk.mbrf.actions.show_portrait_briefing_action import (
    ShowPortraitBriefingAction,
)
from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......model.richchk.unis.unit_id import UnitId
from ......util import logger
from ...helpers.richchk_enum_transcoder import RichChkEnumTranscoder
from ..rich_briefing_action_transcoder import RichBriefingActionTranscoder
from ..rich_briefing_action_transcoder_factory import (
    _RichBriefingActionRegistrableTranscoder,
)


class ShowPortraitBriefingActionTranscoder(
    RichBriefingActionTranscoder[ShowPortraitBriefingAction, DecodedTriggerAction],
    _RichBriefingActionRegistrableTranscoder,
    briefing_action_id=ShowPortraitBriefingAction.action_id(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(ShowPortraitBriefingActionTranscoder.__name__)

    def _decode(
        self,
        decoded_action: DecodedTriggerAction,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> ShowPortraitBriefingAction:
        assert decoded_action.action_id == ShowPortraitBriefingAction.action_id().id
        return ShowPortraitBriefingAction(
            _unit=RichChkEnumTranscoder.decode_enum(
                decoded_action.action_argument_type, UnitId
            ),
            _slot=decoded_action.second_group,
        )

    def _encode(
        self,
        rich_action: ShowPortraitBriefingAction,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTriggerAction:
        return DecodedTriggerAction(
            _location_id=0,
            _text_string_id=0,
            _wav_string_id=0,
            _time=0,
            _first_group=0,
            _second_group=rich_action.slot,
            _action_argument_type=RichChkEnumTranscoder.encode_enum(rich_action.unit),
            _action_id=rich_action.action_id().id,
            _quantifier_or_switch_or_order=0,
            _flags=0,
            _padding=0,
            _mask_flag=0,
        )
