import dataclasses
from abc import ABC

from ...mrgn.rich_location import RichLocation
from ...unis.unit_id import UnitId
from ..enums.unit_order import UnitOrder
from ..extended_player_id import AnyPlayerId
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _OrderActionBase(RichTriggerAction, ABC):
    _group: AnyPlayerId
    _unit: UnitId
    _source_location: RichLocation
    _destination_location: RichLocation
    _order: UnitOrder

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.ORDER

    @property
    def group(self) -> AnyPlayerId:
        return self._group

    @property
    def unit(self) -> UnitId:
        return self._unit

    @property
    def source_location(self) -> RichLocation:
        return self._source_location

    @property
    def destination_location(self) -> RichLocation:
        return self._destination_location

    @property
    def order(self) -> UnitOrder:
        return self._order


@dataclasses.dataclass(frozen=True)
class OrderAction(_RichTriggerActionDefaultsBase, _OrderActionBase):
    pass
