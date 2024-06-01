import dataclasses
from abc import ABC

from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _WaitActionBase(RichTriggerAction, ABC):
    _milliseconds: int

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.WAIT

    @property
    def milliseconds(self) -> int:
        return self._milliseconds


@dataclasses.dataclass(frozen=True)
class WaitAction(_RichTriggerActionDefaultsBase, _WaitActionBase):
    pass
