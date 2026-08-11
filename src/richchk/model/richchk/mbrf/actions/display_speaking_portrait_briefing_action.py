import dataclasses
from abc import ABC

from ..briefing_action_id import BriefingActionId
from ..rich_briefing_action import RichBriefingAction, _RichBriefingActionDefaultsBase


@dataclasses.dataclass(frozen=True)
class _DisplaySpeakingPortraitBriefingActionBase(RichBriefingAction, ABC):
    _slot: int
    _duration_ms: int

    @classmethod
    def action_id(cls) -> BriefingActionId:
        return BriefingActionId.DISPLAY_SPEAKING_PORTRAIT

    @property
    def slot(self) -> int:
        return self._slot

    @property
    def duration_ms(self) -> int:
        return self._duration_ms


@dataclasses.dataclass(frozen=True)
class DisplaySpeakingPortraitBriefingAction(
    _RichBriefingActionDefaultsBase, _DisplaySpeakingPortraitBriefingActionBase
):
    pass
