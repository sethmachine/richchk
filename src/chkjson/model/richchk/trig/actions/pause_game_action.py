import dataclasses
from abc import ABC

from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _PauseGameActionBase(RichTriggerAction, ABC):
    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.PAUSE_GAME


@dataclasses.dataclass(frozen=True)
class PauseGameAction(_RichTriggerActionDefaultsBase, _PauseGameActionBase):
    pass
