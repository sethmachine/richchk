"""Decode No Condition trigger condition."""

from ......model.chk.trig.decoded_trigger_condition import DecodedTriggerCondition
from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......model.richchk.trig.conditions.AlwaysCondition import AlwaysCondition
from ......util import logger
from ..rich_trigger_condition_transcoder import RichTriggerConditionTranscoder
from ..rich_trigger_condition_transcoder_factory import (
    _RichTriggerConditionRegistrableTranscoder,
)


class RichTriggerAlwaysConditionTranscoder(
    RichTriggerConditionTranscoder[AlwaysCondition, DecodedTriggerCondition],
    _RichTriggerConditionRegistrableTranscoder,
    trigger_condition_id=AlwaysCondition.condition_id(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(RichTriggerAlwaysConditionTranscoder.__name__)

    def decode(
        self,
        decoded_condition: DecodedTriggerCondition,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> AlwaysCondition:
        assert decoded_condition.condition_id == AlwaysCondition.condition_id().id
        return AlwaysCondition()

    def encode(
        self,
        rich_condition: AlwaysCondition,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTriggerCondition:
        return DecodedTriggerCondition(
            _location_id=0,
            _group=0,
            _quantity=0,
            _unit_id=0,
            _numeric_comparison_operation=0,
            _condition_id=AlwaysCondition.condition_id().id,
            _numeric_comparand_type=0,
            _flags=0,
            _mask_flag=0,
        )
