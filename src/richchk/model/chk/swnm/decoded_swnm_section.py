"""SWNM - Switch names.

Not Required.

This section contains the strings used for each switch. There are 256 switches, and
can't be any more or any less.

u32[256]: One long for each switch, specifies the string number for the name of each
switch. Unnamed switches will have an index of 0, and have a default switch name.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..decoded_chk_section import DecodedChkSection


@dataclasses.dataclass(frozen=True)
class DecodedSwnmSection(DecodedChkSection):
    """Represent SWNM section for switch names data.

    :param _switch_string_ids: One long for each switch, specifies the string number for
        the name of each switch. Unnamed switches will have an index of 0, and have a
        default switch name.
    """

    _switch_string_ids: list[int]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.SWNM

    @property
    def switch_string_ids(self) -> list[int]:
        return self._switch_string_ids
