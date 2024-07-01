import dataclasses
from abc import ABC

from ...str.rich_string import RichString
from ..enums.score_type import ScoreType
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _LeaderboardShowScoreActionBase(RichTriggerAction, ABC):
    _text: RichString
    _score_type: ScoreType

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.LEADER_BOARD_POINTS

    @property
    def text(self) -> RichString:
        return self._text

    @property
    def score(self) -> ScoreType:
        return self._score_type


@dataclasses.dataclass(frozen=True)
class LeaderboardShowScoreAction(
    _RichTriggerActionDefaultsBase, _LeaderboardShowScoreActionBase
):
    pass
