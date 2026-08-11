import dataclasses
from abc import ABC

from ...unis.unit_id import UnitId
from ..briefing_action_id import BriefingActionId
from ..rich_briefing_action import RichBriefingAction, _RichBriefingActionDefaultsBase


@dataclasses.dataclass(frozen=True)
class _ShowPortraitBriefingActionBase(RichBriefingAction, ABC):
    _unit: UnitId
    _slot: int

    @classmethod
    def action_id(cls) -> BriefingActionId:
        return BriefingActionId.SHOW_PORTRAIT

    @property
    def unit(self) -> UnitId:
        return self._unit

    @property
    def slot(self) -> int:
        return self._slot


@dataclasses.dataclass(frozen=True)
class ShowPortraitBriefingAction(
    _RichBriefingActionDefaultsBase, _ShowPortraitBriefingActionBase
):
    pass
