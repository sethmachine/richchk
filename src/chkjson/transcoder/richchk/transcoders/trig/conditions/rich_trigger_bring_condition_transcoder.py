"""Decode CountdownTimer trigger condition."""
from ......model.chk.trig.decoded_trigger_condition import DecodedTriggerCondition
from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......model.richchk.trig.conditions.bring_condition import BringCondition
from ......model.richchk.trig.conditions.comparators.numeric_comparator import (
    NumericComparator,
)
from ......model.richchk.trig.player_id import PlayerId
from ......model.richchk.unis.unit_id import UnitId
from ......util import logger
from ...helpers.richchk_enum_transcoder import RichChkEnumTranscoder
from ..rich_trigger_condition_transcoder import RichTriggerConditionTranscoder
from ..rich_trigger_condition_transcoder_factory import (
    _RichTriggerConditionRegistrableTranscoder,
)


class RichTriggerBringConditionTranscoder(
    RichTriggerConditionTranscoder[BringCondition, DecodedTriggerCondition],
    _RichTriggerConditionRegistrableTranscoder,
    trigger_condition_id=BringCondition.condition_id(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(RichTriggerBringConditionTranscoder.__name__)

    def decode(
        self,
        decoded_condition: DecodedTriggerCondition,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> BringCondition:
        assert decoded_condition.condition_id == BringCondition.condition_id().id
        return BringCondition(
            _group=RichChkEnumTranscoder.decode_enum(decoded_condition.group, PlayerId),
            _comparator=RichChkEnumTranscoder.decode_enum(
                decoded_condition.numeric_comparison_operation, NumericComparator
            ),
            _quantity=decoded_condition.quantity,
            _unit=RichChkEnumTranscoder.decode_enum(decoded_condition.unit_id, UnitId),
            _location=rich_chk_decode_context.rich_mrgn_lookup.get_location_by_id_or_throw(
                decoded_condition.location_id
            ),
        )

    def encode(
        self,
        rich_condition: BringCondition,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTriggerCondition:
        return DecodedTriggerCondition(
            _location_id=0,
            _group=RichChkEnumTranscoder.encode_enum(rich_condition.group),
            _quantity=rich_condition.quantity,
            _unit_id=RichChkEnumTranscoder.encode_enum(rich_condition.unit),
            _numeric_comparison_operation=RichChkEnumTranscoder.encode_enum(
                rich_condition.comparator
            ),
            _condition_id=rich_condition.condition_id().id,
            _numeric_comparand_type=0,
            _flags=0,
            _mask_flag=0,
        )
