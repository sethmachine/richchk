"""Decode Set Switch trigger action."""
from ......model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......model.richchk.str.rich_string import RichNullString
from ......model.richchk.swnm.rich_switch import RichSwitch
from ......model.richchk.trig.actions.set_switch_action import SetSwitchAction
from ......model.richchk.trig.enums.switch_action import SwitchAction
from ......util import logger
from ...helpers.richchk_enum_transcoder import RichChkEnumTranscoder
from ..rich_trigger_action_transcoder import RichTriggerActionTranscoder
from ..rich_trigger_action_transcoder_factory import (
    _RichTriggerActionRegistrableTranscoder,
)


class RichTriggerSetSwitchActionTranscoder(
    RichTriggerActionTranscoder[SetSwitchAction, DecodedTriggerAction],
    _RichTriggerActionRegistrableTranscoder,
    trigger_action_id=SetSwitchAction.action_id(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(RichTriggerSetSwitchActionTranscoder.__name__)

    def _decode(
        self,
        decoded_action: DecodedTriggerAction,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> SetSwitchAction:
        assert decoded_action.action_id == SetSwitchAction.action_id().id
        return SetSwitchAction(
            _switch=self._decode_switch(
                decoded_action.second_group, rich_chk_decode_context
            ),
            _switch_action=RichChkEnumTranscoder.decode_enum(
                decoded_action.quantifier_or_switch_or_order, SwitchAction
            ),
        )

    def _decode_switch(
        self,
        switch_id: int,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichSwitch:
        maybe_switch = rich_chk_decode_context.rich_swnm_lookup.get_switch_by_id(
            switch_id
        )
        if not maybe_switch:
            return RichSwitch(_custom_name=RichNullString(), _index=switch_id)
        return maybe_switch

    def _encode(
        self,
        rich_action: SetSwitchAction,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTriggerAction:
        return DecodedTriggerAction(
            _location_id=0,
            _text_string_id=0,
            _wav_string_id=0,
            _time=0,
            _first_group=0,
            _second_group=rich_chk_encode_context.rich_swnm_lookup.get_id_by_switch(
                rich_action.switch
            ),
            _action_argument_type=0,
            _action_id=rich_action.action_id().id,
            _quantifier_or_switch_or_order=RichChkEnumTranscoder.encode_enum(
                rich_action.switch_action
            ),
            _flags=0,
            _padding=0,
            _mask_flag=0,
        )
