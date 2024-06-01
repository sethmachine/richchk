"""Decode Least Resources trigger condition."""
from ......model.chk.trig.decoded_trigger_condition import DecodedTriggerCondition
from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......model.richchk.trig.conditions.least_resources_condition import (
    LeastResourcesCondition,
)
from ......model.richchk.trig.enums.resource_type import ResourceType
from ......util import logger
from ...helpers.richchk_enum_transcoder import RichChkEnumTranscoder
from ..rich_trigger_condition_transcoder import RichTriggerConditionTranscoder
from ..rich_trigger_condition_transcoder_factory import (
    _RichTriggerConditionRegistrableTranscoder,
)


class RichTriggerLeastResourcesConditionTranscoder(
    RichTriggerConditionTranscoder[LeastResourcesCondition, DecodedTriggerCondition],
    _RichTriggerConditionRegistrableTranscoder,
    trigger_condition_id=LeastResourcesCondition.condition_id(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(
            RichTriggerLeastResourcesConditionTranscoder.__name__
        )

    def _decode(
        self,
        decoded_condition: DecodedTriggerCondition,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> LeastResourcesCondition:
        assert (
            decoded_condition.condition_id == LeastResourcesCondition.condition_id().id
        )
        return LeastResourcesCondition(
            _resource=RichChkEnumTranscoder.decode_enum(
                decoded_condition.numeric_comparand_type, ResourceType
            )
        )

    def _encode(
        self,
        rich_condition: LeastResourcesCondition,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTriggerCondition:
        return DecodedTriggerCondition(
            _location_id=0,
            _group=0,
            _quantity=0,
            _unit_id=0,
            _numeric_comparison_operation=0,
            _condition_id=rich_condition.condition_id().id,
            _numeric_comparand_type=RichChkEnumTranscoder.encode_enum(
                rich_condition.resource
            ),
            _flags=0,
            _mask_flag=0,
        )
