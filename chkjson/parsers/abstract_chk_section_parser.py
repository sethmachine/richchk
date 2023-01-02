"""

"""

import abc
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
    def compile(self, chk_section: T) -> bytes:
        pass
