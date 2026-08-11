import dataclasses
from abc import ABC

from ..briefing_action_id import BriefingActionId
from ..rich_briefing_action import RichBriefingAction, _RichBriefingActionDefaultsBase


@dataclasses.dataclass(frozen=True)
class _WaitBriefingActionBase(RichBriefingAction, ABC):
    _milliseconds: int

    @classmethod
    def action_id(cls) -> BriefingActionId:
        return BriefingActionId.WAIT

    @property
    def milliseconds(self) -> int:
        return self._milliseconds


@dataclasses.dataclass(frozen=True)
class WaitBriefingAction(_RichBriefingActionDefaultsBase, _WaitBriefingActionBase):
    pass
