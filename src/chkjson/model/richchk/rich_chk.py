"""Represents the ordered list of both rich and decoded CHK sections.

The RichChk contains a mix of rich and decoded CHK sections in order to keep the
original order of sections in Scenario.chk file.  The decoded CHK sections exists for at
least one of the following reasons: (1) there is no need for a human-readable
representation of that decoded CHK section (e.g. STR), or (2) the code to transform
between rich and decoded representations has not been written.

This mixed data structure format is chosen so it is possible to go directly from a
RichChk to an edited and saved .scm/.scx map file.
"""

import copy
import dataclasses
import functools
from collections import defaultdict
from typing import Union

from ...model.chk_section_name import ChkSectionName
from ..chk.decoded_chk_section import DecodedChkSection
from .rich_chk_section import RichChkSection


@dataclasses.dataclass(frozen=True)
class RichChk:
    _chk_sections: list[Union[RichChkSection, DecodedChkSection]]

    @property
    def chk_sections(self) -> list[Union[RichChkSection, DecodedChkSection]]:
        return copy.deepcopy(self._chk_sections)

    @functools.cached_property
    def _sections_by_name(
        self,
    ) -> dict[ChkSectionName, list[Union[RichChkSection, DecodedChkSection]]]:
        sections_by_name = defaultdict(list)
        for section in self._chk_sections:
            sections_by_name[section.section_name()].append(section)
        return sections_by_name

    def get_sections_by_name(
        self, chk_section_name: ChkSectionName
    ) -> list[Union[RichChkSection, DecodedChkSection]]:
        return copy.deepcopy(self._sections_by_name[chk_section_name])
