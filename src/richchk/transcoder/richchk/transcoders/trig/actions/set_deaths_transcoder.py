"""Decode Set Deaths (for units) trigger action."""

from ......model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......model.richchk.trig.actions.set_deaths_action import SetDeathsAction
from ......model.richchk.trig.enums.amount_modifier import AmountModifier
from ......model.richchk.trig.player_id import PlayerId
from ......model.richchk.unis.unit_id import UnitId
from ......util import logger
from ...helpers.richchk_enum_transcoder import RichChkEnumTranscoder
from ..rich_trigger_action_transcoder import RichTriggerActionTranscoder
from ..rich_trigger_action_transcoder_factory import (
    _RichTriggerActionRegistrableTranscoder,
)


class RichTriggerSetDeathsActionTranscoder(
    RichTriggerActionTranscoder[SetDeathsAction, DecodedTriggerAction],
    _RichTriggerActionRegistrableTranscoder,
    trigger_action_id=SetDeathsAction.action_id(),
):
    _ACTION_ID_INT: int = SetDeathsAction.action_id().id

    def __init__(self) -> None:
        self.log = logger.get_logger(RichTriggerSetDeathsActionTranscoder.__name__)

    def _decode(
        self,
        decoded_action: DecodedTriggerAction,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> SetDeathsAction:
        assert decoded_action.action_id == SetDeathsAction.action_id().id
        return SetDeathsAction(
            _group=RichChkEnumTranscoder.decode_enum(
                decoded_action.first_group, PlayerId
            ),
            _amount=decoded_action.second_group,
            _unit=RichChkEnumTranscoder.decode_enum(
                decoded_action.action_argument_type, UnitId
            ),
            _amount_modifier=RichChkEnumTranscoder.decode_enum(
                decoded_action.quantifier_or_switch_or_order, AmountModifier
            ),
        )

    def _encode(
        self,
        rich_action: SetDeathsAction,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTriggerAction:
        return DecodedTriggerAction(
            _location_id=0,
            _text_string_id=0,
            _wav_string_id=0,
            _time=0,
            _first_group=rich_action._group._id,
            _second_group=rich_action._amount,
            _action_argument_type=rich_action._unit._id,
            _action_id=self._ACTION_ID_INT,
            _quantifier_or_switch_or_order=rich_action._amount_modifier._id,
            _flags=0,
            _padding=0,
            _mask_flag=0,
        )
