import dataclasses
from abc import ABC

from ...mrgn.rich_location import RichLocation
from ...unis.unit_id import UnitId
from ..player_id import PlayerId
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _GiveUnitsActionBase(RichTriggerAction, ABC):
    _from_group: PlayerId
    _to_group: PlayerId
    _amount: int
    _unit: UnitId
    _location: RichLocation

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.REMOVE_UNIT_AT_LOCATION

    @property
    def from_group(self) -> PlayerId:
        return self._from_group

    @property
    def to_group(self) -> PlayerId:
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
class GiveUnitsAction(_RichTriggerActionDefaultsBase, _GiveUnitsActionBase):
    pass
