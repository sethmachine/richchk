import dataclasses
from abc import ABC

from ...mrgn.rich_location import RichLocation
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _MinimapPingActionBase(RichTriggerAction, ABC):
    _location: RichLocation

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.MINIMAP_PING

    @property
    def location(self) -> RichLocation:
        return self._location


@dataclasses.dataclass(frozen=True)
class MinimapPingAction(_RichTriggerActionDefaultsBase, _MinimapPingActionBase):
    pass
