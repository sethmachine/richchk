import dataclasses
from abc import ABC
from typing import Any, ClassVar, Optional

from ..actions.flags.trigger_action_flags import (
    _DEFAULT_TRIGGER_ACTION_FLAGS,
    TriggerActionFlags,
)
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _PreserveTriggerActionBase(RichTriggerAction, ABC):
    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.PRESERVE_TRIGGER


@dataclasses.dataclass(frozen=True, init=False)
class PreserveTrigger(_RichTriggerActionDefaultsBase, _PreserveTriggerActionBase):
    _singleton: ClassVar[Optional["PreserveTrigger"]] = None

    def __new__(
        cls, _flags: TriggerActionFlags = _DEFAULT_TRIGGER_ACTION_FLAGS
    ) -> "PreserveTrigger":
        if _flags == _DEFAULT_TRIGGER_ACTION_FLAGS:
            if cls._singleton is None:
                instance = object.__new__(cls)
                instance.__dict__["_flags"] = _DEFAULT_TRIGGER_ACTION_FLAGS
                cls._singleton = instance
            return cls._singleton
        instance = object.__new__(cls)
        instance.__dict__["_flags"] = _flags
        return instance

    def __init__(
        self, _flags: TriggerActionFlags = _DEFAULT_TRIGGER_ACTION_FLAGS
    ) -> None:
        pass

    def __reduce__(self) -> tuple[Any, ...]:
        return (PreserveTrigger, (self._flags,))
