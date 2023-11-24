"""Base model for representing the data in a CHK section.

"""


import dataclasses
from abc import ABC, abstractmethod
from typing import Type, TypeVar

from ..chk_section_name import ChkSectionName

_T = TypeVar("_T", bound="DecodedChkSection", covariant=True)


@dataclasses.dataclass(frozen=True)
class DecodedChkSection(ABC):
    @classmethod
    @abstractmethod
    def section_name(cls) -> ChkSectionName:
        pass

    @classmethod
    def cast(
        cls, decoded_chk_section: "DecodedChkSection", chk_section_type: Type[_T]
    ) -> _T:
        """Cast a DecodedChkSection into an actual specific CHK section type.
        :param decoded_chk_section:
        :param chk_section_type:
        :return:
        """
        fields = dataclasses.fields(decoded_chk_section)
        as_dict = dataclasses.asdict(decoded_chk_section)
        return chk_section_type(*[as_dict[field.name] for field in fields])
