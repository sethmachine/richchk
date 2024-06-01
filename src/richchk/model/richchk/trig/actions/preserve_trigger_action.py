import dataclasses
from abc import ABC

from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _PreserveTriggerActionBase(RichTriggerAction, ABC):
    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.PRESERVE_TRIGGER


@dataclasses.dataclass(frozen=True)
class PreserveTrigger(_RichTriggerActionDefaultsBase, _PreserveTriggerActionBase):
    pass
