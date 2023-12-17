"""Represents the ordered list of rich CHK sections."""

import copy
import dataclasses

from .rich_chk_section import RichChkSection


@dataclasses.dataclass(frozen=True)
class RichChk:
    _rich_chk_sections: list[RichChkSection]

    @property
    def rich_chk_sections(self) -> list[RichChkSection]:
        return copy.deepcopy(self._rich_chk_sections)
