import dataclasses
from abc import ABC

from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _UnpauseGameActionBase(RichTriggerAction, ABC):
    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.UNPAUSE_GAME


@dataclasses.dataclass(frozen=True)
class UnpauseGameAction(_RichTriggerActionDefaultsBase, _UnpauseGameActionBase):
    pass
