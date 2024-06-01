import dataclasses

from ..enums.score_type import ScoreType
from ..rich_trigger_condition import (
    RichTriggerCondition,
    _RichTriggerConditionDefaultsBase,
)
from ..trigger_condition_id import TriggerConditionId


@dataclasses.dataclass(frozen=True)
class _LowestScoreConditionBase(RichTriggerCondition):

    _score_type: ScoreType

    @classmethod
    def condition_id(cls) -> TriggerConditionId:
        return TriggerConditionId.LOWEST_SCORE

    @property
    def score_type(self) -> ScoreType:
        return self._score_type


@dataclasses.dataclass(frozen=True)
class LowestScoreCondition(
    _RichTriggerConditionDefaultsBase,
    _LowestScoreConditionBase,
):
    pass
