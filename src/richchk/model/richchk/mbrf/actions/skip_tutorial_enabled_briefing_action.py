import dataclasses
from abc import ABC

from ..briefing_action_id import BriefingActionId
from ..rich_briefing_action import RichBriefingAction, _RichBriefingActionDefaultsBase


@dataclasses.dataclass(frozen=True)
class _SkipTutorialEnabledBriefingActionBase(RichBriefingAction, ABC):
    @classmethod
    def action_id(cls) -> BriefingActionId:
        return BriefingActionId.SKIP_TUTORIAL_ENABLED


@dataclasses.dataclass(frozen=True)
class SkipTutorialEnabledBriefingAction(
    _RichBriefingActionDefaultsBase, _SkipTutorialEnabledBriefingActionBase
):
    pass
