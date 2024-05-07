"""Represents a trigger action."""

import dataclasses
from abc import ABC, abstractmethod

from .trigger_condition_id import TriggerConditionId


@dataclasses.dataclass(frozen=True)
class RichTriggerCondition(ABC):
    @classmethod
    @abstractmethod
    def condition_id(cls) -> TriggerConditionId:
        pass
