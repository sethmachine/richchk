"""Represents a trigger action."""

import dataclasses
from abc import ABC, abstractmethod

from .conditions.flags.trigger_condition_flags import TriggerConditionFlags
from .trigger_condition_id import TriggerConditionId


@dataclasses.dataclass(frozen=True)
class _RichTriggerConditionDefaultsBase(ABC):
    _flags: TriggerConditionFlags = TriggerConditionFlags()

    @property
    def flags(self) -> TriggerConditionFlags:
        return self._flags


@dataclasses.dataclass(frozen=True)
class RichTriggerCondition(ABC):
    @classmethod
    @abstractmethod
    def condition_id(cls) -> TriggerConditionId:
        pass

    # this is a hack so the type checker does not complain.  Hard to do TypeVar with multiple inheritance
    @property
    @abstractmethod
    def flags(self) -> TriggerConditionFlags:
        pass
