import dataclasses

from ...unis.unit_id import UnitId
from ..player_id import PlayerId
from ..rich_trigger_condition import (
    RichTriggerCondition,
    _RichTriggerConditionDefaultsBase,
)
from ..trigger_condition_id import TriggerConditionId
from .comparators.numeric_comparator import NumericComparator
from .flags.trigger_condition_flags import (
    _DEFAULT_TRIGGER_CONDITION_FLAGS,
    TriggerConditionFlags,
)


@dataclasses.dataclass(frozen=True)
class _DeathsConditionBase(RichTriggerCondition):

    _group: PlayerId
    _comparator: NumericComparator
    _amount: int
    _unit: UnitId

    @classmethod
    def condition_id(cls) -> TriggerConditionId:
        return TriggerConditionId.DEATHS

    @property
    def group(self) -> PlayerId:
        return self._group

    @property
    def comparator(self) -> NumericComparator:
        return self._comparator

    @property
    def amount(self) -> int:
        return self._amount

    @property
    def unit(self) -> UnitId:
        return self._unit


@dataclasses.dataclass(frozen=True, init=False)
class DeathsCondition(
    _RichTriggerConditionDefaultsBase,
    _DeathsConditionBase,
):
    def __init__(
        self,
        _group: PlayerId,
        _comparator: NumericComparator,
        _amount: int,
        _unit: UnitId,
        _flags: TriggerConditionFlags = _DEFAULT_TRIGGER_CONDITION_FLAGS,
    ) -> None:
        self.__dict__.update(
            {
                "_group": _group,
                "_comparator": _comparator,
                "_amount": _amount,
                "_unit": _unit,
                "_flags": _flags,
            }
        )
