"""Represents an abstract class for decoding trigger actions into rich trigger
actions."""

from abc import abstractmethod
from typing import Any, Protocol, TypeVar, runtime_checkable

from chkjson.model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from chkjson.model.richchk.richchk_decode_context import RichChkDecodeContext
from chkjson.model.richchk.richchk_encode_context import RichChkEncodeContext
from chkjson.model.richchk.trig.rich_trigger_action import RichTriggerAction

_T = TypeVar("_T", bound=RichTriggerAction, contravariant=True)
_U = TypeVar("_U", bound=DecodedTriggerAction, contravariant=False, covariant=False)


@runtime_checkable
class RichTriggerActionTranscoder(Protocol[_T, _U]):
    def __call__(self, *args: list[Any], **kwargs: dict[str, Any]) -> Any:
        return self

    @abstractmethod
    def decode(
        self, decoded_action: _U, rich_chk_decode_context: RichChkDecodeContext
    ) -> RichTriggerAction:
        raise NotImplementedError

    @abstractmethod
    def encode(
        self, rich_action: _T, rich_chk_encode_context: RichChkEncodeContext
    ) -> _U:
        raise NotImplementedError
