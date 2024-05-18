import dataclasses

from ..rich_trigger_condition import RichTriggerCondition
from ..trigger_condition_id import TriggerConditionId


@dataclasses.dataclass(frozen=True)
class NoConditionCondition(RichTriggerCondition):
    @classmethod
    def condition_id(cls) -> TriggerConditionId:
        return TriggerConditionId.NO_CONDITION
