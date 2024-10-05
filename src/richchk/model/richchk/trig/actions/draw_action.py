import dataclasses
from abc import ABC

from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _DrawActionBase(RichTriggerAction, ABC):
    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.DRAW


@dataclasses.dataclass(frozen=True)
class DrawAction(_RichTriggerActionDefaultsBase, _DrawActionBase):
    pass
