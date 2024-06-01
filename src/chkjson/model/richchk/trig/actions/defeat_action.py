import dataclasses
from abc import ABC

from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _DefeatActionBase(RichTriggerAction, ABC):
    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.DEFEAT


@dataclasses.dataclass(frozen=True)
class DefeatAction(_RichTriggerActionDefaultsBase, _DefeatActionBase):
    pass
