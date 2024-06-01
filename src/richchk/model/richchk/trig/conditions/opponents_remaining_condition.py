import dataclasses

from ..player_id import PlayerId
from ..rich_trigger_condition import (
    RichTriggerCondition,
    _RichTriggerConditionDefaultsBase,
)
from ..trigger_condition_id import TriggerConditionId
from .comparators.numeric_comparator import NumericComparator


@dataclasses.dataclass(frozen=True)
class _OpponentsRemainingConditionBase(RichTriggerCondition):

    _group: PlayerId
    _amount: int
    _comparator: NumericComparator

    @classmethod
    def condition_id(cls) -> TriggerConditionId:
        return TriggerConditionId.OPPONENTS

    @property
    def group(self) -> PlayerId:
        return self._group

    @property
    def amount(self) -> int:
        return self._amount

    @property
    def comparator(self) -> NumericComparator:
        return self._comparator


@dataclasses.dataclass(frozen=True)
class OpponentsRemainingCondition(
    _RichTriggerConditionDefaultsBase,
    _OpponentsRemainingConditionBase,
):
    pass
