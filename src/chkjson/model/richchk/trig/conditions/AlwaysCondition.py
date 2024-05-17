import dataclasses

from ..rich_trigger_condition import RichTriggerCondition
from ..trigger_condition_id import TriggerConditionId


@dataclasses.dataclass(frozen=True)
class AlwaysCondition(RichTriggerCondition):
    @classmethod
    def condition_id(cls) -> TriggerConditionId:
        return TriggerConditionId.ALWAYS
