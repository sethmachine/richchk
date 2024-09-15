import dataclasses
from abc import ABC

from ...mrgn.rich_location import RichLocation
from ...unis.unit_id import UnitId
from ..enums.doodad_action import DoodadAction
from ..player_id import PlayerId
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _SetDoodadStateActionBase(RichTriggerAction, ABC):
    _group: PlayerId
    _unit: UnitId
    _location: RichLocation
    _doodad_action: DoodadAction

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.SET_DOODAD_STATE

    @property
    def group(self) -> PlayerId:
        return self._group

    @property
    def unit(self) -> UnitId:
        return self._unit

    @property
    def location(self) -> RichLocation:
        return self._location

    @property
    def doodad_action(self) -> DoodadAction:
        return self._doodad_action


@dataclasses.dataclass(frozen=True)
class SetDoodadStateAction(_RichTriggerActionDefaultsBase, _SetDoodadStateActionBase):
    pass
