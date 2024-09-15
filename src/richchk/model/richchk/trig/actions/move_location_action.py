"""Center a location on a unit type owned by a player in another location.

This how locations can be "moved" around the map.  This centers the "source_location" on
a unit type owned by another player (or force/group) which is located in the
"destination_location."

Often times the "destination_location" is "Anywhere", but can be more restrictive
depending upon needs or how the map may be divided.
"""
import dataclasses
from abc import ABC

from ...mrgn.rich_location import RichLocation
from ...unis.unit_id import UnitId
from ..player_id import PlayerId
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _MoveLocationActionBase(RichTriggerAction, ABC):
    _source_location: RichLocation
    _unit: UnitId
    _group: PlayerId
    _destination_location: RichLocation

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.MOVE_LOCATION

    @property
    def source_location(self) -> RichLocation:
        return self._source_location

    @property
    def unit(self) -> UnitId:
        return self._unit

    @property
    def group(self) -> PlayerId:
        return self._group

    @property
    def destination_location(self) -> RichLocation:
        return self._destination_location


@dataclasses.dataclass(frozen=True)
class MoveLocationAction(_RichTriggerActionDefaultsBase, _MoveLocationActionBase):
    pass
