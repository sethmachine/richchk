import dataclasses

from ..enums.resource_type import ResourceType
from ..player_id import PlayerId
from ..rich_trigger_condition import (
    RichTriggerCondition,
    _RichTriggerConditionDefaultsBase,
)
from ..trigger_condition_id import TriggerConditionId
from .comparators.numeric_comparator import NumericComparator


@dataclasses.dataclass(frozen=True)
class _AccumulateResourcesConditionBase(RichTriggerCondition):
    _group: PlayerId
    _comparator: NumericComparator
    _amount: int
    _resource: ResourceType

    @classmethod
    def condition_id(cls) -> TriggerConditionId:
        return TriggerConditionId.ACCUMULATE

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
    def resource(self) -> ResourceType:
        return self._resource


@dataclasses.dataclass(frozen=True)
class AccumulateResourcesCondition(
    _RichTriggerConditionDefaultsBase,
    _AccumulateResourcesConditionBase,
):
    pass
