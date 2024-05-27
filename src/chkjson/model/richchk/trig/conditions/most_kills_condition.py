import dataclasses

from ...unis.unit_id import UnitId
from ..player_id import PlayerId
from ..rich_trigger_condition import (
    RichTriggerCondition,
    _RichTriggerConditionDefaultsBase,
)
from ..trigger_condition_id import TriggerConditionId


@dataclasses.dataclass(frozen=True)
class _MostKillsConditionBase(RichTriggerCondition):
    _group: PlayerId
    _unit: UnitId

    @classmethod
    def condition_id(cls) -> TriggerConditionId:
        return TriggerConditionId.MOST_KILLS

    @property
    def group(self) -> PlayerId:
        return self._group

    @property
    def unit(self) -> UnitId:
        return self._unit


@dataclasses.dataclass(frozen=True)
class MostKillsCondition(
    _RichTriggerConditionDefaultsBase,
    _MostKillsConditionBase,
):
    pass
