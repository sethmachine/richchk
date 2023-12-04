"""Represents an abstract class for decoding and encoding binary CHK section data."""

import struct
from abc import abstractmethod
from typing import Any, Protocol, TypeVar, runtime_checkable

from ..model.chk.decoded_chk_section import DecodedChkSection
from ..model.chk_section_name import ChkSectionName

_T = TypeVar("_T", bound=DecodedChkSection, contravariant=True)


@runtime_checkable
class ChkSectionTranscoder(Protocol[_T]):
    def __call__(self, *args: list[Any], **kwargs: dict[str, Any]) -> Any:
        pass

    @abstractmethod
    def decode(self, chk_section_binary_data: bytes) -> DecodedChkSection:
        raise NotImplementedError

    def encode(self, decoded_chk_section: _T) -> bytes:
        chk_binary_data = self._encode(decoded_chk_section)
        return (
            self._encode_chk_section_header(
                decoded_chk_section.section_name(), len(chk_binary_data)
            )
            + chk_binary_data
        )

    @abstractmethod
    def _encode(self, decoded_chk_section: _T) -> bytes:
        raise NotImplementedError

    @classmethod
    def _encode_chk_section_header(
        cls, chk_section_name: ChkSectionName, chk_binary_data_size: int
    ) -> bytes:
        data: bytes = b""
        data += struct.pack(
            "{}s".format(len(chk_section_name.value)),
            bytes(chk_section_name.value, "utf-8"),
        )
        data += struct.pack("I", chk_binary_data_size)
        return data
