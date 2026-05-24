"""Represents an abstract class for decoding trigger actions into rich trigger
actions."""

import dataclasses
from abc import abstractmethod
from typing import Any, Protocol, TypeVar, runtime_checkable

from .....model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from .....model.richchk.richchk_decode_context import RichChkDecodeContext
from .....model.richchk.richchk_encode_context import RichChkEncodeContext
from .....model.richchk.trig.actions.flags.trigger_action_flags import (
    _DEFAULT_TRIGGER_ACTION_FLAGS,
)
from .....model.richchk.trig.rich_trigger_action import RichTriggerAction
from .....transcoder.richchk.transcoders.helpers.trigger_action_flags_transcoder import (
    TriggerActionFlagsTranscoder,
)

_T = TypeVar("_T", bound=RichTriggerAction, contravariant=True)
_U = TypeVar("_U", bound=DecodedTriggerAction, contravariant=False, covariant=False)


@runtime_checkable
class RichTriggerActionTranscoder(Protocol[_T, _U]):
    def __call__(self, *args: list[Any], **kwargs: dict[str, Any]) -> Any:
        return self

    def decode(
        self, decoded_action: _U, rich_chk_decode_context: RichChkDecodeContext
    ) -> RichTriggerAction:
        flags_int = decoded_action.flags
        rich = self._decode(decoded_action, rich_chk_decode_context)
        if flags_int == 0:
            return rich
        return dataclasses.replace(
            rich,
            _flags=TriggerActionFlagsTranscoder.decode_flags(flags_int),
        )  # type: ignore[call-arg]

    @abstractmethod
    def _decode(
        self, decoded_action: _U, rich_chk_decode_context: RichChkDecodeContext
    ) -> RichTriggerAction:
        raise NotImplementedError

    def encode(
        self, rich_action: _T, rich_chk_encode_context: RichChkEncodeContext
    ) -> _U:
        decoded = self._encode(rich_action, rich_chk_encode_context)
        # Identity check: almost all actions use the shared default flags singleton.
        # This avoids calling encode_flags() (5 bool→int conversions) in the common case.
        if rich_action.flags is _DEFAULT_TRIGGER_ACTION_FLAGS:
            return decoded
        flags_int = TriggerActionFlagsTranscoder.encode_flags(rich_action.flags)
        if flags_int == 0:
            return decoded
        return dataclasses.replace(decoded, _flags=flags_int)

    @abstractmethod
    def _encode(
        self, rich_action: _T, rich_chk_encode_context: RichChkEncodeContext
    ) -> _U:
        raise NotImplementedError
