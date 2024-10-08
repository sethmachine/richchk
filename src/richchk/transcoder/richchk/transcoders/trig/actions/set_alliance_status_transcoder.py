"""Decode Alliance Status action."""

from ......model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......model.richchk.trig.actions.set_alliance_status_action import (
    SetAllianceStatusAction,
)
from ......model.richchk.trig.enums.alliance_status import AllianceStatus
from ......model.richchk.trig.player_id import PlayerId
from ......util import logger
from ...helpers.richchk_enum_transcoder import RichChkEnumTranscoder
from ..rich_trigger_action_transcoder import RichTriggerActionTranscoder
from ..rich_trigger_action_transcoder_factory import (
    _RichTriggerActionRegistrableTranscoder,
)


class RichTriggerSetAllianceStatusActionTranscoder(
    RichTriggerActionTranscoder[SetAllianceStatusAction, DecodedTriggerAction],
    _RichTriggerActionRegistrableTranscoder,
    trigger_action_id=SetAllianceStatusAction.action_id(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(
            RichTriggerSetAllianceStatusActionTranscoder.__name__
        )

    def _decode(
        self,
        decoded_action: DecodedTriggerAction,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> SetAllianceStatusAction:
        assert decoded_action.action_id == SetAllianceStatusAction.action_id().id
        return SetAllianceStatusAction(
            _group=RichChkEnumTranscoder.decode_enum(
                decoded_action.first_group, PlayerId
            ),
            _alliance_status=RichChkEnumTranscoder.decode_enum(
                decoded_action.action_argument_type, AllianceStatus
            ),
        )

    def _encode(
        self,
        rich_action: SetAllianceStatusAction,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTriggerAction:
        return DecodedTriggerAction(
            _location_id=0,
            _text_string_id=0,
            _wav_string_id=0,
            _time=0,
            _first_group=RichChkEnumTranscoder.encode_enum(rich_action.group),
            _second_group=0,
            _action_argument_type=RichChkEnumTranscoder.encode_enum(
                rich_action.alliance_status
            ),
            _action_id=rich_action.action_id().id,
            _quantifier_or_switch_or_order=0,
            _flags=0,
            _padding=0,
            _mask_flag=0,
        )
