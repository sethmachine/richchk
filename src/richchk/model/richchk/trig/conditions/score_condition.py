import dataclasses

from ..enums.score_type import ScoreType
from ..player_id import PlayerId
from ..rich_trigger_condition import (
    RichTriggerCondition,
    _RichTriggerConditionDefaultsBase,
)
from ..trigger_condition_id import TriggerConditionId
from .comparators.numeric_comparator import NumericComparator


@dataclasses.dataclass(frozen=True)
class _ScoreConditionBase(RichTriggerCondition):

    _group: PlayerId
    _comparator: NumericComparator
    _amount: int
    _score_type: ScoreType

    @classmethod
    def condition_id(cls) -> TriggerConditionId:
        return TriggerConditionId.SCORE

    @property
    def group(self) -> PlayerId:
        return self._group

    @property
    def comparator(self) -> NumericComparator:
        return self._comparator

    @property
    def amount(self) -> int:
        return self._amount

    @property
    def score_type(self) -> ScoreType:
        return self._score_type


@dataclasses.dataclass(frozen=True)
class ScoreCondition(
    _RichTriggerConditionDefaultsBase,
    _ScoreConditionBase,
):
    pass
