"""Decode Command Least At trigger condition."""
from ......model.chk.trig.decoded_trigger_condition import DecodedTriggerCondition
from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......model.richchk.trig.conditions.command_least_at_condition import (
    CommandLeastAtCondition,
)
from ......model.richchk.unis.unit_id import UnitId
from ......util import logger
from ...helpers.richchk_enum_transcoder import RichChkEnumTranscoder
from ..rich_trigger_condition_transcoder import RichTriggerConditionTranscoder
from ..rich_trigger_condition_transcoder_factory import (
    _RichTriggerConditionRegistrableTranscoder,
)


class RichTriggerCommandLeastAtConditionTranscoder(
    RichTriggerConditionTranscoder[CommandLeastAtCondition, DecodedTriggerCondition],
    _RichTriggerConditionRegistrableTranscoder,
    trigger_condition_id=CommandLeastAtCondition.condition_id(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(
            RichTriggerCommandLeastAtConditionTranscoder.__name__
        )

    def _decode(
        self,
        decoded_condition: DecodedTriggerCondition,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> CommandLeastAtCondition:
        assert (
            decoded_condition.condition_id == CommandLeastAtCondition.condition_id().id
        )
        return CommandLeastAtCondition(
            _unit=RichChkEnumTranscoder.decode_enum(decoded_condition.unit_id, UnitId),
            _location=rich_chk_decode_context.rich_mrgn_lookup.get_location_by_id_or_throw(
                decoded_condition.location_id
            ),
        )

    def _encode(
        self,
        rich_condition: CommandLeastAtCondition,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTriggerCondition:
        return DecodedTriggerCondition(
            _location_id=rich_chk_encode_context.rich_mrgn_lookup.get_id_by_location_or_throw(
                rich_condition.location
            ),
            _group=0,
            _quantity=0,
            _unit_id=RichChkEnumTranscoder.encode_enum(rich_condition.unit),
            _numeric_comparison_operation=0,
            _condition_id=rich_condition.condition_id().id,
            _numeric_comparand_type=0,
            _flags=0,
            _mask_flag=0,
        )
