"""Base model for representing the data in a CHK section.

"""

import abc
import dataclasses

from chkjson.model.chk.chk_section_names import ChkSectionName


@dataclasses.dataclass
class BaseChkSection(abc.ABC):
    name: ChkSectionName
    data: bytes
