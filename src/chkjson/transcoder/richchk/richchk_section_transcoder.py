"""Represents an abstract class for decoding DecodedChk to RichChk."""

from abc import abstractmethod
from typing import Any, Protocol, TypeVar, runtime_checkable

from ...model.chk.decoded_chk_section import DecodedChkSection
from ...model.richchk.rich_chk_section import RichChkSection
from ...model.richchk.richchk_decode_context import RichChkDecodeContext
from ...model.richchk.richchk_encode_context import RichChkEncodeContext

_T = TypeVar("_T", bound=RichChkSection, contravariant=True)
_U = TypeVar("_U", bound=DecodedChkSection, contravariant=False, covariant=False)


@runtime_checkable
class RichChkSectionTranscoder(Protocol[_T, _U]):
    def __call__(self, *args: list[Any], **kwargs: dict[str, Any]) -> Any:
        return self

    @abstractmethod
    def decode(
        self, decoded_chk_section: _U, rich_chk_decode_context: RichChkDecodeContext
    ) -> RichChkSection:
        raise NotImplementedError

    @abstractmethod
    def encode(
        self, rich_chk_section: _T, rich_chk_encode_context: RichChkEncodeContext
    ) -> _U:
        raise NotImplementedError
