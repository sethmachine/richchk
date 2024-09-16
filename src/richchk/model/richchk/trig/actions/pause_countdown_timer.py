import dataclasses
from abc import ABC

from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _PauseCountdownTimerActionBase(RichTriggerAction, ABC):
    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.PAUSE_TIMER


@dataclasses.dataclass(frozen=True)
class PauseCountdownTimerAction(
    _RichTriggerActionDefaultsBase, _PauseCountdownTimerActionBase
):
    pass
