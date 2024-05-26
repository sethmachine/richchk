"""Represents an abstract class for decoding trigger actions into rich trigger
actions."""

from abc import abstractmethod
from typing import Any, Protocol, TypeVar, runtime_checkable

from chkjson.model.chk.trig.decoded_trigger_condition import DecodedTriggerCondition
from chkjson.model.richchk.richchk_decode_context import RichChkDecodeContext
from chkjson.model.richchk.richchk_encode_context import RichChkEncodeContext
from chkjson.model.richchk.trig.rich_trigger_condition import RichTriggerCondition
from chkjson.transcoder.richchk.transcoders.helpers.trigger_condition_flags_transcoder import (
    TriggerConditionFlagsTranscoder,
)
from chkjson.util.dataclasses_util import build_dataclass_with_fields

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
        return build_dataclass_with_fields(
            self._decode(
                decoded_condition,
                rich_chk_decode_context,
            ),
            _flags=TriggerConditionFlagsTranscoder.decode_flags(
                decoded_condition.flags
            ),
        )

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
        return build_dataclass_with_fields(
            self._encode(rich_condition, rich_chk_encode_context),
            _flags=TriggerConditionFlagsTranscoder.encode_flags(rich_condition.flags),
        )

    @abstractmethod
    def _encode(
        self, rich_condition: _T, rich_chk_encode_context: RichChkEncodeContext
    ) -> _U:
        raise NotImplementedError
