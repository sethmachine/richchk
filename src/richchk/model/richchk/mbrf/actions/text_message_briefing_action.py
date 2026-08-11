import dataclasses
from abc import ABC

from ...str.rich_string import RichString
from ..briefing_action_id import BriefingActionId
from ..rich_briefing_action import RichBriefingAction, _RichBriefingActionDefaultsBase


@dataclasses.dataclass(frozen=True)
class _TextMessageBriefingActionBase(RichBriefingAction, ABC):
    _text: RichString
    _duration_ms: int

    @classmethod
    def action_id(cls) -> BriefingActionId:
        return BriefingActionId.TEXT_MESSAGE

    @property
    def message(self) -> RichString:
        return self._text

    @property
    def duration_ms(self) -> int:
        return self._duration_ms


@dataclasses.dataclass(frozen=True)
class TextMessageBriefingAction(
    _RichBriefingActionDefaultsBase, _TextMessageBriefingActionBase
):
    pass
