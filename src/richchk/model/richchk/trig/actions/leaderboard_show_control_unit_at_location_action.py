import dataclasses
from abc import ABC

from ...mrgn.rich_location import RichLocation
from ...str.rich_string import RichString
from ...unis.unit_id import UnitId
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _LeaderboardShowControlUnitAtLocationActionBase(RichTriggerAction, ABC):
    _text: RichString
    _unit: UnitId
    _location: RichLocation

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.LEADER_BOARD_CONTROL_AT_LOCATION

    @property
    def text(self) -> RichString:
        return self._text

    @property
    def unit(self) -> UnitId:
        return self._unit

    @property
    def location(self) -> RichLocation:
        return self._location


@dataclasses.dataclass(frozen=True)
class LeaderboardShowControlUnitAtLocationAction(
    _RichTriggerActionDefaultsBase, _LeaderboardShowControlUnitAtLocationActionBase
):
    pass
