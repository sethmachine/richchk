import dataclasses
from abc import ABC

from ..enums.amount_modifier import AmountModifier
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _SetCountdownTimerActionBase(RichTriggerAction, ABC):
    _seconds: int
    _amount_modifier: AmountModifier

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.SET_COUNTDOWN_TIMER

    @property
    def seconds(self) -> int:
        return self._seconds

    @property
    def amount_modifier(self) -> AmountModifier:
        return self._amount_modifier


@dataclasses.dataclass(frozen=True)
class SetCountdownTimerAction(
    _RichTriggerActionDefaultsBase, _SetCountdownTimerActionBase
):
    pass
