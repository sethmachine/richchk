import dataclasses
from abc import ABC

from ...swnm.rich_switch import RichSwitch
from ..enums.switch_action import SwitchAction
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _SetSwitchActionBase(RichTriggerAction, ABC):
    _switch: RichSwitch
    _switch_action: SwitchAction

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.SET_SWITCH

    @property
    def switch(self) -> RichSwitch:
        return self._switch

    @property
    def switch_action(self) -> SwitchAction:
        return self._switch_action


@dataclasses.dataclass(frozen=True)
class SetSwitchAction(_RichTriggerActionDefaultsBase, _SetSwitchActionBase):
    pass
