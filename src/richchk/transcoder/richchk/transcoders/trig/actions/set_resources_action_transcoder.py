"""Set resources action."""

from ......model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......model.richchk.trig.actions.set_resources_action import SetResourcesAction
from ......model.richchk.trig.enums.amount_modifier import AmountModifier
from ......model.richchk.trig.enums.resource_type import ResourceType
from ......model.richchk.trig.player_id import PlayerId
from ......util import logger
from ...helpers.richchk_enum_transcoder import RichChkEnumTranscoder
from ..rich_trigger_action_transcoder import RichTriggerActionTranscoder
from ..rich_trigger_action_transcoder_factory import (
    _RichTriggerActionRegistrableTranscoder,
)


class RichTriggerSetResourcesActionTranscoder(
    RichTriggerActionTranscoder[SetResourcesAction, DecodedTriggerAction],
    _RichTriggerActionRegistrableTranscoder,
    trigger_action_id=SetResourcesAction.action_id(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(RichTriggerSetResourcesActionTranscoder.__name__)

    def _decode(
        self,
        decoded_action: DecodedTriggerAction,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> SetResourcesAction:
        assert decoded_action.action_id == SetResourcesAction.action_id().id
        return SetResourcesAction(
            _group=RichChkEnumTranscoder.decode_enum(
                decoded_action.first_group, PlayerId
            ),
            _amount_modifier=RichChkEnumTranscoder.decode_enum(
                decoded_action.quantifier_or_switch_or_order, AmountModifier
            ),
            _amount=decoded_action.second_group,
            _resource=RichChkEnumTranscoder.decode_enum(
                decoded_action.action_argument_type, ResourceType
            ),
        )

    def _encode(
        self,
        rich_action: SetResourcesAction,
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
                rich_action.resource
            ),
            _action_id=rich_action.action_id().id,
            _quantifier_or_switch_or_order=RichChkEnumTranscoder.encode_enum(
                rich_action.amount_modifier
            ),
            _flags=0,
            _padding=0,
            _mask_flag=0,
        )
