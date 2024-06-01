import dataclasses

from ..enums.resource_type import ResourceType
from ..rich_trigger_condition import (
    RichTriggerCondition,
    _RichTriggerConditionDefaultsBase,
)
from ..trigger_condition_id import TriggerConditionId


@dataclasses.dataclass(frozen=True)
class _LeastResourcesConditionBase(RichTriggerCondition):

    _resource: ResourceType

    @classmethod
    def condition_id(cls) -> TriggerConditionId:
        return TriggerConditionId.LEAST_RESOURCES

    @property
    def resource(self) -> ResourceType:
        return self._resource


@dataclasses.dataclass(frozen=True)
class LeastResourcesCondition(
    _RichTriggerConditionDefaultsBase,
    _LeastResourcesConditionBase,
):
    pass
