import dataclasses

from ...unis.unit_id import UnitId
from ..rich_trigger_condition import (
    RichTriggerCondition,
    _RichTriggerConditionDefaultsBase,
)
from ..trigger_condition_id import TriggerConditionId


@dataclasses.dataclass(frozen=True)
class _CommandLeastConditionBase(RichTriggerCondition):

    _unit: UnitId

    @classmethod
    def condition_id(cls) -> TriggerConditionId:
        return TriggerConditionId.COMMAND_THE_LEAST

    @property
    def unit(self) -> UnitId:
        return self._unit


@dataclasses.dataclass(frozen=True)
class CommandLeastCondition(
    _RichTriggerConditionDefaultsBase,
    _CommandLeastConditionBase,
):
    pass
