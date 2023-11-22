"""Base model for representing the data in a CHK section.

"""

import abc
import dataclasses

from chkjson.model.chk_section_name import ChkSectionName


@dataclasses.dataclass(frozen=True)
class DecodedChkSection(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def section_name(cls) -> ChkSectionName:
        pass
