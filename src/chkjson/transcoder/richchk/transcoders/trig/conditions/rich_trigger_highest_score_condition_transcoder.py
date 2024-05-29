"""Decode Highest Score trigger condition."""
from ......model.chk.trig.decoded_trigger_condition import DecodedTriggerCondition
from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......model.richchk.trig.conditions.highest_score_condition import (
    HighestScoreCondition,
)
from ......model.richchk.trig.enums.score_type import ScoreType
from ......util import logger
from ...helpers.richchk_enum_transcoder import RichChkEnumTranscoder
from ..rich_trigger_condition_transcoder import RichTriggerConditionTranscoder
from ..rich_trigger_condition_transcoder_factory import (
    _RichTriggerConditionRegistrableTranscoder,
)


class RichTriggerHighestScoreConditionTranscoder(
    RichTriggerConditionTranscoder[HighestScoreCondition, DecodedTriggerCondition],
    _RichTriggerConditionRegistrableTranscoder,
    trigger_condition_id=HighestScoreCondition.condition_id(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(
            RichTriggerHighestScoreConditionTranscoder.__name__
        )

    def _decode(
        self,
        decoded_condition: DecodedTriggerCondition,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> HighestScoreCondition:
        assert decoded_condition.condition_id == HighestScoreCondition.condition_id().id
        return HighestScoreCondition(
            _score_type=RichChkEnumTranscoder.decode_enum(
                decoded_condition.numeric_comparand_type, ScoreType
            )
        )

    def _encode(
        self,
        rich_condition: HighestScoreCondition,
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
                rich_condition.score_type
            ),
            _flags=0,
            _mask_flag=0,
        )
