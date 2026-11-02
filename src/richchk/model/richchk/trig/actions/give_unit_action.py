import dataclasses
from abc import ABC

from ...mrgn.rich_location import RichLocation
from ...unis.unit_id import UnitId
from ..extended_player_id import AnyPlayerId
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _GiveUnitActionBase(RichTriggerAction, ABC):
    _from_group: AnyPlayerId
    _to_group: AnyPlayerId
    _amount: int
    _unit: UnitId
    _location: RichLocation

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.GIVE_UNITS_TO_PLAYER

    @property
    def from_group(self) -> AnyPlayerId:
        return self._from_group

    @property
    def to_group(self) -> AnyPlayerId:
        return self._to_group

    @property
    def unit(self) -> UnitId:
        return self._unit

    @property
    def amount(self) -> int:
        return self._amount

    @property
    def location(self) -> RichLocation:
        return self._location


@dataclasses.dataclass(frozen=True)
class GiveUnitAction(_RichTriggerActionDefaultsBase, _GiveUnitActionBase):
    pass
