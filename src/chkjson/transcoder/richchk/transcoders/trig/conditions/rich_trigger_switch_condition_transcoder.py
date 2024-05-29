"""Decode Switch state trigger condition."""
from ......model.chk.trig.decoded_trigger_condition import DecodedTriggerCondition
from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......model.richchk.str.rich_string import RichNullString
from ......model.richchk.swnm.rich_switch import RichSwitch
from ......model.richchk.trig.conditions.switch_condition import SwitchCondition
from ......model.richchk.trig.enums.switch_state import SwitchState
from ......util import logger
from ...helpers.richchk_enum_transcoder import RichChkEnumTranscoder
from ..rich_trigger_condition_transcoder import RichTriggerConditionTranscoder
from ..rich_trigger_condition_transcoder_factory import (
    _RichTriggerConditionRegistrableTranscoder,
)


class RichTriggerSwitchConditionTranscoder(
    RichTriggerConditionTranscoder[SwitchCondition, DecodedTriggerCondition],
    _RichTriggerConditionRegistrableTranscoder,
    trigger_condition_id=SwitchCondition.condition_id(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(RichTriggerSwitchConditionTranscoder.__name__)

    def _decode(
        self,
        decoded_condition: DecodedTriggerCondition,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> SwitchCondition:
        assert decoded_condition.condition_id == SwitchCondition.condition_id().id
        return SwitchCondition(
            _switch_state=RichChkEnumTranscoder.decode_enum(
                decoded_condition.numeric_comparison_operation, SwitchState
            ),
            _switch=self._decode_switch(
                switch_id=decoded_condition.numeric_comparand_type,
                rich_chk_decode_context=rich_chk_decode_context,
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
        rich_condition: SwitchCondition,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTriggerCondition:
        if rich_condition.switch_state is None:
            msg = (
                f"RichSwitch does not have an index allocated.  "
                f"All switch usages must be allocated an index [0,255].  "
                f"Condition with switch usage: {rich_condition}."
            )
            self.log.error(msg)
            raise ValueError(msg)
        assert rich_condition.switch.index is not None
        return DecodedTriggerCondition(
            _location_id=0,
            _group=0,
            _quantity=0,
            _unit_id=0,
            _numeric_comparison_operation=RichChkEnumTranscoder.encode_enum(
                rich_condition.switch_state
            ),
            _condition_id=rich_condition.condition_id().id,
            _numeric_comparand_type=rich_condition.switch.index,
            _flags=0,
            _mask_flag=0,
        )
