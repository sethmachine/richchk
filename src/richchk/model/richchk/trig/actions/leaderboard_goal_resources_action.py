import dataclasses
from abc import ABC

from ...str.rich_string import RichString
from ..enums.resource_type import ResourceType
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _LeaderboardGoalResourcesActionBase(RichTriggerAction, ABC):
    _text: RichString
    _resource: ResourceType
    _goal: int

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.LEADERBOARD_GOAL_RESOURCES

    @property
    def text(self) -> RichString:
        return self._text

    @property
    def resource(self) -> ResourceType:
        return self._resource

    @property
    def goal(self) -> int:
        return self._goal


@dataclasses.dataclass(frozen=True)
class LeaderboardGoalResourcesAction(
    _RichTriggerActionDefaultsBase, _LeaderboardGoalResourcesActionBase
):
    pass
