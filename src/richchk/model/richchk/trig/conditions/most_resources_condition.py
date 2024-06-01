import dataclasses

from ..enums.resource_type import ResourceType
from ..rich_trigger_condition import (
    RichTriggerCondition,
    _RichTriggerConditionDefaultsBase,
)
from ..trigger_condition_id import TriggerConditionId


@dataclasses.dataclass(frozen=True)
class _MostResourcesConditionBase(RichTriggerCondition):

    _resource: ResourceType

    @classmethod
    def condition_id(cls) -> TriggerConditionId:
        return TriggerConditionId.MOST_RESOURCES

    @property
    def resource(self) -> ResourceType:
        return self._resource


@dataclasses.dataclass(frozen=True)
class MostResourcesCondition(
    _RichTriggerConditionDefaultsBase,
    _MostResourcesConditionBase,
):
    pass
