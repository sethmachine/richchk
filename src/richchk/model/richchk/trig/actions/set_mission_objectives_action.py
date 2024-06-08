import dataclasses
from abc import ABC

from ...str.rich_string import RichString
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _SetMissionObjectivesActionBase(RichTriggerAction, ABC):
    _text: RichString

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.SET_MISSION_OBJECTIVES

    @property
    def message(self) -> RichString:
        return self._text


@dataclasses.dataclass(frozen=True)
class SetMissionObjectivesAction(
    _RichTriggerActionDefaultsBase, _SetMissionObjectivesActionBase
):
    pass
