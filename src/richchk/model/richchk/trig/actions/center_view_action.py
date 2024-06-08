import dataclasses
from abc import ABC

from ...mrgn.rich_location import RichLocation
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _CenterViewActionBase(RichTriggerAction, ABC):
    _location: RichLocation

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.CENTER_VIEW

    @property
    def location(self) -> RichLocation:
        return self._location


@dataclasses.dataclass(frozen=True)
class CenterViewAction(_RichTriggerActionDefaultsBase, _CenterViewActionBase):
    pass
