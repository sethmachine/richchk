"""Represents a mission briefing action."""

import dataclasses
from abc import ABC, abstractmethod

from .actions.flags.briefing_action_flags import (
    _DEFAULT_BRIEFING_ACTION_FLAGS,
    BriefingActionFlags,
)
from .briefing_action_id import BriefingActionId


@dataclasses.dataclass(frozen=True)
class _RichBriefingActionDefaultsBase(ABC):
    _flags: BriefingActionFlags = _DEFAULT_BRIEFING_ACTION_FLAGS

    @property
    def flags(self) -> BriefingActionFlags:
        return self._flags


@dataclasses.dataclass(frozen=True)
class RichBriefingAction(ABC):
    @classmethod
    @abstractmethod
    def action_id(cls) -> BriefingActionId:
        pass

    @property
    @abstractmethod
    def flags(self) -> BriefingActionFlags:
        pass
