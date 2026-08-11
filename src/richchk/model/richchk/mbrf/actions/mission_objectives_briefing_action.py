import dataclasses
from abc import ABC

from ...str.rich_string import RichString
from ..briefing_action_id import BriefingActionId
from ..rich_briefing_action import RichBriefingAction, _RichBriefingActionDefaultsBase


@dataclasses.dataclass(frozen=True)
class _MissionObjectivesBriefingActionBase(RichBriefingAction, ABC):
    _text: RichString

    @classmethod
    def action_id(cls) -> BriefingActionId:
        return BriefingActionId.MISSION_OBJECTIVES

    @property
    def message(self) -> RichString:
        return self._text


@dataclasses.dataclass(frozen=True)
class MissionObjectivesBriefingAction(
    _RichBriefingActionDefaultsBase, _MissionObjectivesBriefingActionBase
):
    pass
