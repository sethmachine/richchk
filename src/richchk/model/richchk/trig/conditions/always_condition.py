import dataclasses

from ..rich_trigger_condition import (
    RichTriggerCondition,
    _RichTriggerConditionDefaultsBase,
)
from ..trigger_condition_id import TriggerConditionId


@dataclasses.dataclass(frozen=True)
class _AlwaysConditionBase(RichTriggerCondition):
    @classmethod
    def condition_id(cls) -> TriggerConditionId:
        return TriggerConditionId.ALWAYS


@dataclasses.dataclass(frozen=True)
class AlwaysCondition(
    _RichTriggerConditionDefaultsBase,
    _AlwaysConditionBase,
):
    pass
