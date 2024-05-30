import dataclasses

from ..rich_trigger_condition import (
    RichTriggerCondition,
    _RichTriggerConditionDefaultsBase,
)
from ..trigger_condition_id import TriggerConditionId


@dataclasses.dataclass(frozen=True)
class _NeverConditionBase(RichTriggerCondition):
    @classmethod
    def condition_id(cls) -> TriggerConditionId:
        return TriggerConditionId.NEVER


@dataclasses.dataclass(frozen=True)
class NeverCondition(
    _RichTriggerConditionDefaultsBase,
    _NeverConditionBase,
):
    pass
