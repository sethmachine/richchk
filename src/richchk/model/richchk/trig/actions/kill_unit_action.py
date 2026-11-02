import dataclasses
from abc import ABC

from ...unis.unit_id import UnitId
from ..extended_player_id import AnyPlayerId
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _KillUnitActionBase(RichTriggerAction, ABC):
    _group: AnyPlayerId
    _unit: UnitId

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.KILL_UNIT

    @property
    def group(self) -> AnyPlayerId:
        return self._group

    @property
    def unit(self) -> UnitId:
        return self._unit


@dataclasses.dataclass(frozen=True)
class KillUnitAction(_RichTriggerActionDefaultsBase, _KillUnitActionBase):
    pass
