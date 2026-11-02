import dataclasses
from abc import ABC

from ...mrgn.rich_location import RichLocation
from ...unis.unit_id import UnitId
from ..extended_player_id import AnyPlayerId
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _CreateUnitActionBase(RichTriggerAction, ABC):
    _group: AnyPlayerId
    _amount: int
    _unit: UnitId
    _location: RichLocation

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.CREATE_UNIT

    @property
    def group(self) -> AnyPlayerId:
        return self._group

    @property
    def amount(self) -> int:
        return self._amount

    @property
    def unit(self) -> UnitId:
        return self._unit

    @property
    def location(self) -> RichLocation:
        return self._location


@dataclasses.dataclass(frozen=True)
class CreateUnitAction(_RichTriggerActionDefaultsBase, _CreateUnitActionBase):
    pass
