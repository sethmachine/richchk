"""Base model for representing the human-readable representation of a CHK section."""


import dataclasses
from abc import ABC, abstractmethod
from typing import Type, TypeVar

from ..chk_section_name import ChkSectionName

_T = TypeVar("_T", bound="RichChkSection", covariant=True)


@dataclasses.dataclass(frozen=True)
class RichChkSection(ABC):
    @classmethod
    @abstractmethod
    def section_name(cls) -> ChkSectionName:
        pass

    @classmethod
    def cast(cls, rich_chk_section: "RichChkSection", chk_section_type: Type[_T]) -> _T:
        """Cast a RichChkSection into an actual specific CHK section type.

        :param rich_chk_section:
        :param chk_section_type:
        :return:
        """
        assert isinstance(rich_chk_section, chk_section_type)
        return rich_chk_section
