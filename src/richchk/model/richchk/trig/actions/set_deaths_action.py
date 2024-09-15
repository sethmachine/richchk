import dataclasses
from abc import ABC

from ...unis.unit_id import UnitId
from ..enums.amount_modifier import AmountModifier
from ..player_id import PlayerId
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _SetDeathsActionBase(RichTriggerAction, ABC):
    _group: PlayerId
    _unit: UnitId
    _amount: int
    _amount_modifier: AmountModifier

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.SET_DEATHS

    @property
    def group(self) -> PlayerId:
        return self._group

    @property
    def unit(self) -> UnitId:
        return self._unit

    @property
    def amount(self) -> int:
        return self._amount

    @property
    def amount_modifier(self) -> AmountModifier:
        return self._amount_modifier


@dataclasses.dataclass(frozen=True)
class SetDeathsAction(_RichTriggerActionDefaultsBase, _SetDeathsActionBase):
    pass
