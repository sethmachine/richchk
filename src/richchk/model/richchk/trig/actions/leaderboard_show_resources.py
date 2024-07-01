import dataclasses
from abc import ABC

from ...str.rich_string import RichString
from ..enums.resource_type import ResourceType
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _LeaderboardShowResourcesActionBase(RichTriggerAction, ABC):
    _text: RichString
    _resource: ResourceType

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.LEADER_BOARD_RESOURCES

    @property
    def text(self) -> RichString:
        return self._text

    @property
    def resource(self) -> ResourceType:
        return self._resource


@dataclasses.dataclass(frozen=True)
class LeaderboardShowResourcesAction(
    _RichTriggerActionDefaultsBase, _LeaderboardShowResourcesActionBase
):
    pass
