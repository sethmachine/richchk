import dataclasses
from abc import ABC

from ...mrgn.rich_location import RichLocation
from ...unis.unit_id import UnitId
from ..player_id import PlayerId
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _MoveUnitActionBase(RichTriggerAction, ABC):
    _unit: UnitId
    _group: PlayerId
    _amount: int
    _source_location: RichLocation
    _destination_location: RichLocation

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.MOVE_UNIT

    @property
    def unit(self) -> UnitId:
        return self._unit

    @property
    def group(self) -> PlayerId:
        return self._group

    @property
    def amount(self) -> int:
        return self._amount

    @property
    def source_location(self) -> RichLocation:
        return self._source_location

    @property
    def destination_location(self) -> RichLocation:
        return self._destination_location


@dataclasses.dataclass(frozen=True)
class MoveUnitAction(_RichTriggerActionDefaultsBase, _MoveUnitActionBase):
    pass
