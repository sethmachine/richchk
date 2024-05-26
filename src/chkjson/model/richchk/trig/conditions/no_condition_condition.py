import dataclasses

from ..rich_trigger_condition import (
    RichTriggerCondition,
    _RichTriggerConditionDefaultsBase,
)
from ..trigger_condition_id import TriggerConditionId


@dataclasses.dataclass(frozen=True)
class _NoConditionConditionBase(RichTriggerCondition):
    @classmethod
    def condition_id(cls) -> TriggerConditionId:
        return TriggerConditionId.NO_CONDITION


@dataclasses.dataclass(frozen=True)
class NoConditionCondition(
    _RichTriggerConditionDefaultsBase,
    _NoConditionConditionBase,
):
    pass
