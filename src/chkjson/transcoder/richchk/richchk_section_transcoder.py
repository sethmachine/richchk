"""Represents an abstract class for decoding DecodedChk to RichChk."""

from abc import abstractmethod
from typing import Any, Protocol, TypeVar, runtime_checkable

from ...model.chk.decoded_chk_section import DecodedChkSection
from ...model.richchk.rich_chk_section import RichChkSection

_T = TypeVar("_T", bound=RichChkSection, contravariant=True)
_U = TypeVar("_U", bound=DecodedChkSection, contravariant=False, covariant=False)


@runtime_checkable
class RichChkSectionTranscoder(Protocol[_T, _U]):
    def __call__(self, *args: list[Any], **kwargs: dict[str, Any]) -> Any:
        pass

    @abstractmethod
    def decode(self, decoded_chk_section: _U) -> RichChkSection:
        raise NotImplementedError

    @abstractmethod
    def encode(self, rich_chk_section: _T) -> _U:
        raise NotImplementedError
