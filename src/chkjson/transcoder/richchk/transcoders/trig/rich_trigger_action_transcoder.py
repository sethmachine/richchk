"""Represents an abstract class for decoding trigger actions into rich trigger
actions."""

from abc import abstractmethod
from typing import Any, Protocol, TypeVar, runtime_checkable

from chkjson.model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from chkjson.model.richchk.richchk_decode_context import RichChkDecodeContext
from chkjson.model.richchk.richchk_encode_context import RichChkEncodeContext
from chkjson.model.richchk.trig.rich_trigger_action import RichTriggerAction
from chkjson.transcoder.richchk.transcoders.helpers.trigger_action_flags_transcoder import (
    TriggerActionFlagsTranscoder,
)
from chkjson.util.dataclasses_util import build_dataclass_with_fields

_T = TypeVar("_T", bound=RichTriggerAction, contravariant=True)
_U = TypeVar("_U", bound=DecodedTriggerAction, contravariant=False, covariant=False)


@runtime_checkable
class RichTriggerActionTranscoder(Protocol[_T, _U]):
    def __call__(self, *args: list[Any], **kwargs: dict[str, Any]) -> Any:
        return self

    def decode(
        self, decoded_action: _U, rich_chk_decode_context: RichChkDecodeContext
    ) -> RichTriggerAction:
        return build_dataclass_with_fields(
            self._decode(
                decoded_action,
                rich_chk_decode_context,
            ),
            _flags=TriggerActionFlagsTranscoder.decode_flags(decoded_action.flags),
        )

    @abstractmethod
    def _decode(
        self, decoded_action: _U, rich_chk_decode_context: RichChkDecodeContext
    ) -> RichTriggerAction:
        raise NotImplementedError

    def encode(
        self, rich_action: _T, rich_chk_encode_context: RichChkEncodeContext
    ) -> _U:
        return build_dataclass_with_fields(
            self._encode(
                rich_action,
                rich_chk_encode_context,
            ),
            _flags=TriggerActionFlagsTranscoder.encode_flags(rich_action.flags),
        )

    @abstractmethod
    def _encode(
        self, rich_action: _T, rich_chk_encode_context: RichChkEncodeContext
    ) -> _U:
        raise NotImplementedError
