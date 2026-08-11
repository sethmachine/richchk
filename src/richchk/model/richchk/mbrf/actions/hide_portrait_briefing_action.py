import dataclasses
from abc import ABC

from ..briefing_action_id import BriefingActionId
from ..rich_briefing_action import RichBriefingAction, _RichBriefingActionDefaultsBase


@dataclasses.dataclass(frozen=True)
class _HidePortraitBriefingActionBase(RichBriefingAction, ABC):
    _slot: int

    @classmethod
    def action_id(cls) -> BriefingActionId:
        return BriefingActionId.HIDE_PORTRAIT

    @property
    def slot(self) -> int:
        return self._slot


@dataclasses.dataclass(frozen=True)
class HidePortraitBriefingAction(
    _RichBriefingActionDefaultsBase, _HidePortraitBriefingActionBase
):
    pass
