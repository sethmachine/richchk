"""

"""

import abc
import struct
from typing import Generic, TypeVar

from chkjson.model.chk.base_chk_section import BaseChkSection
from chkjson.model.chk.chk_section_names import ChkSectionName

T = TypeVar("T", bound=BaseChkSection)


class AbstractChkSectionParser(abc.ABC, Generic[T]):
    @property
    @abc.abstractmethod
    def chk_section_name(self) -> ChkSectionName:
        pass

    @abc.abstractmethod
    def parse(self, data: bytes) -> T:
        pass

    @abc.abstractmethod
    def compile(self, chk_section: T, include_header=True) -> bytes:
        pass

    def _compile_header(self, chk_section: T) -> bytes:
        data = b""
        data += struct.pack(
            "{}s".format(len(chk_section.name.value)),
            bytes(chk_section.name.value, "utf-8"),
        )
        data += struct.pack("I", len(chk_section.data))
        return data
