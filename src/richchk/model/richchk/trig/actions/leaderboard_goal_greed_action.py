import dataclasses
from abc import ABC

from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _LeaderboardGoalGreedActionBase(RichTriggerAction, ABC):
    _goal: int

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.LEADERBOARD_GREED

    @property
    def goal(self) -> int:
        return self._goal


@dataclasses.dataclass(frozen=True)
class LeaderboardGoalGreedAction(
    _RichTriggerActionDefaultsBase, _LeaderboardGoalGreedActionBase
):
    pass
