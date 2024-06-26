import dataclasses
from abc import ABC

from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _VictoryActionBase(RichTriggerAction, ABC):
    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.VICTORY


@dataclasses.dataclass(frozen=True)
class VictoryAction(_RichTriggerActionDefaultsBase, _VictoryActionBase):
    pass
