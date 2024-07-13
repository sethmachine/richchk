import dataclasses
from abc import ABC

from ...str.rich_string import RichString
from ..enums.score_type import ScoreType
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _LeaderboardGoalScoreActionBase(RichTriggerAction, ABC):
    _text: RichString
    _score_type: ScoreType
    _goal: int

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.LEADERBOARD_GOAL_POINTS

    @property
    def text(self) -> RichString:
        return self._text

    @property
    def score(self) -> ScoreType:
        return self._score_type

    @property
    def goal(self) -> int:
        return self._goal


@dataclasses.dataclass(frozen=True)
class LeaderboardGoalScoreAction(
    _RichTriggerActionDefaultsBase, _LeaderboardGoalScoreActionBase
):
    pass
