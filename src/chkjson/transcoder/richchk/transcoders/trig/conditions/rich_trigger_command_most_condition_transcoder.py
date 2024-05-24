"""Decode CountdownTimer trigger condition."""
from ......model.chk.trig.decoded_trigger_condition import DecodedTriggerCondition
from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......model.richchk.trig.conditions.command_most_condition import (
    CommandMostCondition,
)
from ......model.richchk.trig.player_id import PlayerId
from ......model.richchk.unis.unit_id import UnitId
from ......util import logger
from ...helpers.richchk_enum_transcoder import RichChkEnumTranscoder
from ..rich_trigger_condition_transcoder import RichTriggerConditionTranscoder
from ..rich_trigger_condition_transcoder_factory import (
    _RichTriggerConditionRegistrableTranscoder,
)


class RichTriggerCommandMostConditionTranscoder(
    RichTriggerConditionTranscoder[CommandMostCondition, DecodedTriggerCondition],
    _RichTriggerConditionRegistrableTranscoder,
    trigger_condition_id=CommandMostCondition.condition_id(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(RichTriggerCommandMostConditionTranscoder.__name__)

    def decode(
        self,
        decoded_condition: DecodedTriggerCondition,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> CommandMostCondition:
        assert decoded_condition.condition_id == CommandMostCondition.condition_id().id
        return CommandMostCondition(
            _group=RichChkEnumTranscoder.decode_enum(decoded_condition.group, PlayerId),
            _unit=RichChkEnumTranscoder.decode_enum(decoded_condition.unit_id, UnitId),
        )

    def encode(
        self,
        rich_condition: CommandMostCondition,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTriggerCondition:
        return DecodedTriggerCondition(
            _location_id=0,
            _group=RichChkEnumTranscoder.encode_enum(rich_condition.group),
            _quantity=0,
            _unit_id=RichChkEnumTranscoder.encode_enum(rich_condition.unit),
            _numeric_comparison_operation=0,
            _condition_id=rich_condition.condition_id().id,
            _numeric_comparand_type=0,
            # means a unit type/ID is used?
            _flags=16,
            _mask_flag=0,
        )
