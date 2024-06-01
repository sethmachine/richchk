import dataclasses

from ...swnm.rich_switch import RichSwitch
from ..enums.switch_state import SwitchState
from ..rich_trigger_condition import (
    RichTriggerCondition,
    _RichTriggerConditionDefaultsBase,
)
from ..trigger_condition_id import TriggerConditionId


@dataclasses.dataclass(frozen=True)
class _SwitchConditionBase(RichTriggerCondition):

    _switch_state: SwitchState
    _switch: RichSwitch

    @classmethod
    def condition_id(cls) -> TriggerConditionId:
        return TriggerConditionId.SWITCH

    @property
    def switch_state(self) -> SwitchState:
        return self._switch_state

    @property
    def switch(self) -> RichSwitch:
        return self._switch


@dataclasses.dataclass(frozen=True)
class SwitchCondition(
    _RichTriggerConditionDefaultsBase,
    _SwitchConditionBase,
):
    pass
