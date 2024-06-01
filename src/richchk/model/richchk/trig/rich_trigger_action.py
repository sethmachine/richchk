"""Represents a trigger action."""

import dataclasses
from abc import ABC, abstractmethod

from .actions.flags.trigger_action_flags import TriggerActionFlags
from .trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _RichTriggerActionDefaultsBase(ABC):
    _flags: TriggerActionFlags = TriggerActionFlags()

    @property
    def flags(self) -> TriggerActionFlags:
        return self._flags


@dataclasses.dataclass(frozen=True)
class RichTriggerAction(ABC):
    @classmethod
    @abstractmethod
    def action_id(cls) -> TriggerActionId:
        pass

    # this is a hack so the type checker does not complain.  Hard to do TypeVar with multiple inheritance
    @property
    @abstractmethod
    def flags(self) -> TriggerActionFlags:
        pass
