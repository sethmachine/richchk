import dataclasses
from abc import ABC

from ...str.rich_string import RichString
from ...unis.unit_id import UnitId
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _LeaderboardGoalControlUnitActionBase(RichTriggerAction, ABC):
    _text: RichString
    _unit: UnitId
    _goal: int

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.LEADERBOARD_GOAL_CONTROL

    @property
    def text(self) -> RichString:
        return self._text

    @property
    def unit(self) -> UnitId:
        return self._unit

    @property
    def goal(self) -> int:
        return self._goal


@dataclasses.dataclass(frozen=True)
class LeaderboardGoalControlUnitAction(
    _RichTriggerActionDefaultsBase, _LeaderboardGoalControlUnitActionBase
):
    pass
