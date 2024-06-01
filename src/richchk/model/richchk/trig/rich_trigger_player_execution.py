"""Represents a trigger action."""

import dataclasses
from abc import ABC, abstractmethod

from .trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class RichTriggerAction(ABC):
    @classmethod
    @abstractmethod
    def action_id(cls) -> TriggerActionId:
        pass
