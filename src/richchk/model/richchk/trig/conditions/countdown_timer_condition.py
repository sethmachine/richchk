import dataclasses

from ..rich_trigger_condition import (
    RichTriggerCondition,
    _RichTriggerConditionDefaultsBase,
)
from ..trigger_condition_id import TriggerConditionId
from .comparators.numeric_comparator import NumericComparator


@dataclasses.dataclass(frozen=True)
class _CountdownTimerConditionBase(RichTriggerCondition):

    _seconds: int
    _comparator: NumericComparator

    @classmethod
    def condition_id(cls) -> TriggerConditionId:
        return TriggerConditionId.COUNTDOWN_TIMER

    @property
    def seconds(self) -> int:
        return self._seconds

    @property
    def comparator(self) -> NumericComparator:
        return self._comparator


@dataclasses.dataclass(frozen=True)
class CountdownTimerCondition(
    _RichTriggerConditionDefaultsBase,
    _CountdownTimerConditionBase,
):
    pass
