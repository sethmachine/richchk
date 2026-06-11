"""Represents an abstract class for decoding trigger actions into rich trigger
actions."""

import dataclasses
from abc import abstractmethod
from typing import Any, Protocol, TypeVar, runtime_checkable

from .....model.chk.trig.decoded_trigger_condition import DecodedTriggerCondition
from .....model.richchk.richchk_decode_context import RichChkDecodeContext
from .....model.richchk.richchk_encode_context import RichChkEncodeContext
from .....model.richchk.trig.conditions.flags.trigger_condition_flags import (
    _DEFAULT_TRIGGER_CONDITION_FLAGS,
)
from .....model.richchk.trig.rich_trigger_condition import RichTriggerCondition
from .....transcoder.richchk.transcoders.helpers.trigger_condition_flags_transcoder import (
    TriggerConditionFlagsTranscoder,
)

_T = TypeVar(
    "_T",
    bound=RichTriggerCondition,
    contravariant=True,
)
_U = TypeVar("_U", bound=DecodedTriggerCondition, contravariant=False, covariant=False)


@runtime_checkable
class RichTriggerConditionTranscoder(Protocol[_T, _U]):
    def __call__(self, *args: list[Any], **kwargs: dict[str, Any]) -> Any:
        return self

    def decode(
        self, decoded_condition: _U, rich_chk_decode_context: RichChkDecodeContext
    ) -> RichTriggerCondition:
        flags_int = decoded_condition.flags
        rich = self._decode(decoded_condition, rich_chk_decode_context)
        if flags_int == 0:
            return rich
        return dataclasses.replace(
            rich,
            _flags=TriggerConditionFlagsTranscoder.decode_flags(flags_int),
        )  # type: ignore[call-arg]

    @abstractmethod
    def _decode(
        self,
        decoded_condition: _U,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichTriggerCondition:
        raise NotImplementedError

    def encode(
        self, rich_condition: _T, rich_chk_encode_context: RichChkEncodeContext
    ) -> _U:
        decoded = self._encode(rich_condition, rich_chk_encode_context)
        # Identity check: almost all conditions use the shared default flags singleton.
        if rich_condition.flags is _DEFAULT_TRIGGER_CONDITION_FLAGS:
            return decoded
        flags_int = TriggerConditionFlagsTranscoder.encode_flags(rich_condition.flags)
        if flags_int == 0:
            return decoded
        return dataclasses.replace(decoded, _flags=flags_int)

    @abstractmethod
    def _encode(
        self, rich_condition: _T, rich_chk_encode_context: RichChkEncodeContext
    ) -> _U:
        raise NotImplementedError
