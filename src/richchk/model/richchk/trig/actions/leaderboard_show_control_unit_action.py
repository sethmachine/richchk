import dataclasses
from abc import ABC

from ...str.rich_string import RichString
from ...unis.unit_id import UnitId
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _LeaderboardShowControlUnitActionBase(RichTriggerAction, ABC):
    _text: RichString
    _unit: UnitId

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.LEADER_BOARD_CONTROL

    @property
    def text(self) -> RichString:
        return self._text

    @property
    def unit(self) -> UnitId:
        return self._unit


@dataclasses.dataclass(frozen=True)
class LeaderboardShowControlUnitAction(
    _RichTriggerActionDefaultsBase, _LeaderboardShowControlUnitActionBase
):
    pass
