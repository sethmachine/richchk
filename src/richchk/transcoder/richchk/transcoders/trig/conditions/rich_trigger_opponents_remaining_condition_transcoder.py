"""Decode OpponentsRemaining trigger condition."""
from ......model.chk.trig.decoded_trigger_condition import DecodedTriggerCondition
from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......model.richchk.trig.conditions.comparators.numeric_comparator import (
    NumericComparator,
)
from ......model.richchk.trig.conditions.opponents_remaining_condition import (
    OpponentsRemainingCondition,
)
from ......model.richchk.trig.player_id import PlayerId
from ......util import logger
from ...helpers.richchk_enum_transcoder import RichChkEnumTranscoder
from ..rich_trigger_condition_transcoder import RichTriggerConditionTranscoder
from ..rich_trigger_condition_transcoder_factory import (
    _RichTriggerConditionRegistrableTranscoder,
)


class RichTriggerOpponentsRemainingConditionTranscoder(
    RichTriggerConditionTranscoder[
        OpponentsRemainingCondition, DecodedTriggerCondition
    ],
    _RichTriggerConditionRegistrableTranscoder,
    trigger_condition_id=OpponentsRemainingCondition.condition_id(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(
            RichTriggerOpponentsRemainingConditionTranscoder.__name__
        )

    def _decode(
        self,
        decoded_condition: DecodedTriggerCondition,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> OpponentsRemainingCondition:
        assert (
            decoded_condition.condition_id
            == OpponentsRemainingCondition.condition_id().id
        )
        return OpponentsRemainingCondition(
            _group=RichChkEnumTranscoder.decode_enum(decoded_condition.group, PlayerId),
            _comparator=RichChkEnumTranscoder.decode_enum(
                decoded_condition.numeric_comparison_operation, NumericComparator
            ),
            _amount=decoded_condition.quantity,
        )

    def _encode(
        self,
        rich_condition: OpponentsRemainingCondition,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTriggerCondition:
        return DecodedTriggerCondition(
            _location_id=0,
            _group=RichChkEnumTranscoder.encode_enum(rich_condition.group),
            _quantity=rich_condition.amount,
            _unit_id=0,
            _numeric_comparison_operation=RichChkEnumTranscoder.encode_enum(
                rich_condition.comparator
            ),
            _condition_id=rich_condition.condition_id().id,
            _numeric_comparand_type=0,
            _flags=0,
            _mask_flag=0,
        )
