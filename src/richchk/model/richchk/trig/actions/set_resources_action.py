import dataclasses
from abc import ABC

from ..enums.amount_modifier import AmountModifier
from ..enums.resource_type import ResourceType
from ..extended_player_id import AnyPlayerId
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _SetResourcesActionBase(RichTriggerAction, ABC):
    _group: AnyPlayerId
    _amount_modifier: AmountModifier
    _amount: int
    _resource: ResourceType

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.SET_RESOURCES

    @property
    def group(self) -> AnyPlayerId:
        return self._group

    @property
    def amount(self) -> int:
        return self._amount

    @property
    def amount_modifier(self) -> AmountModifier:
        return self._amount_modifier

    @property
    def resource(self) -> ResourceType:
        return self._resource


@dataclasses.dataclass(frozen=True)
class SetResourcesAction(_RichTriggerActionDefaultsBase, _SetResourcesActionBase):
    pass
