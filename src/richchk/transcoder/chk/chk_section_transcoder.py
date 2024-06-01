"""Represents an abstract class for decoding and encoding binary CHK section data."""

import struct
from abc import abstractmethod
from typing import Any, Protocol, TypeVar, Union, runtime_checkable

from ...model.chk.decoded_chk_section import DecodedChkSection
from ...model.chk_section_name import ChkSectionName
from ...transcoder.chk.strings_common import _STRING_ENCODING

_T = TypeVar("_T", bound=DecodedChkSection, contravariant=True)


@runtime_checkable
class ChkSectionTranscoder(Protocol[_T]):
    def __call__(self, *args: list[Any], **kwargs: dict[str, Any]) -> Any:
        return self

    @abstractmethod
    def decode(self, chk_section_binary_data: bytes) -> DecodedChkSection:
        raise NotImplementedError

    def encode(self, decoded_chk_section: _T, include_header: bool = True) -> bytes:
        chk_binary_data = self._encode(decoded_chk_section)
        if include_header:
            return (
                self.encode_chk_section_header(
                    decoded_chk_section.section_name(), len(chk_binary_data)
                )
                + chk_binary_data
            )
        return chk_binary_data

    @abstractmethod
    def _encode(self, decoded_chk_section: _T) -> bytes:
        raise NotImplementedError

    @classmethod
    def encode_chk_section_header(
        cls, chk_section_name: Union[ChkSectionName, str], chk_binary_data_size: int
    ) -> bytes:
        if isinstance(chk_section_name, ChkSectionName):
            raw_section_name: str = chk_section_name.value
        else:
            raw_section_name = chk_section_name
        data: bytes = b""
        data += struct.pack(
            "{}s".format(len(raw_section_name)),
            bytes(raw_section_name, _STRING_ENCODING),
        )
        data += struct.pack("I", chk_binary_data_size)
        return data
