"""Abstract protocol for decoding mission briefing actions into rich briefing
actions."""

import dataclasses
from abc import abstractmethod
from typing import Any, Protocol, TypeVar, runtime_checkable

from .....model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from .....model.richchk.mbrf.actions.flags.briefing_action_flags import (
    _DEFAULT_BRIEFING_ACTION_FLAGS,
)
from .....model.richchk.mbrf.rich_briefing_action import RichBriefingAction
from .....model.richchk.richchk_decode_context import RichChkDecodeContext
from .....model.richchk.richchk_encode_context import RichChkEncodeContext
from .....transcoder.richchk.transcoders.helpers.briefing_action_flags_transcoder import (
    BriefingActionFlagsTranscoder,
)

_T = TypeVar("_T", bound=RichBriefingAction, contravariant=True)
_U = TypeVar("_U", bound=DecodedTriggerAction, contravariant=False, covariant=False)


@runtime_checkable
class RichBriefingActionTranscoder(Protocol[_T, _U]):
    def __call__(self, *args: list[Any], **kwargs: dict[str, Any]) -> Any:
        return self

    def decode(
        self, decoded_action: _U, rich_chk_decode_context: RichChkDecodeContext
    ) -> RichBriefingAction:
        flags_int = decoded_action.flags
        rich = self._decode(decoded_action, rich_chk_decode_context)
        if flags_int == 0:
            return rich
        return dataclasses.replace(
            rich,
            _flags=BriefingActionFlagsTranscoder.decode_flags(flags_int),
        )  # type: ignore[call-arg]

    @abstractmethod
    def _decode(
        self, decoded_action: _U, rich_chk_decode_context: RichChkDecodeContext
    ) -> RichBriefingAction:
        raise NotImplementedError

    def encode(
        self, rich_action: _T, rich_chk_encode_context: RichChkEncodeContext
    ) -> _U:
        decoded = self._encode(rich_action, rich_chk_encode_context)
        if rich_action.flags is _DEFAULT_BRIEFING_ACTION_FLAGS:
            return decoded
        flags_int = BriefingActionFlagsTranscoder.encode_flags(rich_action.flags)
        if flags_int == 0:
            return decoded
        return dataclasses.replace(decoded, _flags=flags_int)

    @abstractmethod
    def _encode(
        self, rich_action: _T, rich_chk_encode_context: RichChkEncodeContext
    ) -> _U:
        raise NotImplementedError
