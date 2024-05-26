import dataclasses

from ...mrgn.rich_location import RichLocation
from ...unis.unit_id import UnitId
from ..player_id import PlayerId
from ..rich_trigger_condition import (
    RichTriggerCondition,
    _RichTriggerConditionDefaultsBase,
)
from ..trigger_condition_id import TriggerConditionId


@dataclasses.dataclass(frozen=True)
class _CommandMostAtConditionBase(RichTriggerCondition):

    _group: PlayerId
    _unit: UnitId
    _location: RichLocation

    @classmethod
    def condition_id(cls) -> TriggerConditionId:
        return TriggerConditionId.COMMAND_THE_MOST

    @property
    def group(self) -> PlayerId:
        return self._group

    @property
    def unit(self) -> UnitId:
        return self._unit

    @property
    def location(self) -> RichLocation:
        return self._location


@dataclasses.dataclass(frozen=True)
class CommandMostAtCondition(
    _RichTriggerConditionDefaultsBase,
    _CommandMostAtConditionBase,
):
    pass
