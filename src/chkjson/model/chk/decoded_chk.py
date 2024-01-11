"""Represents the ordered list of decoded CHK sections from a decoded CHK file."""

import dataclasses
import functools
from collections import defaultdict
from copy import deepcopy

from ...model.chk_section_name import ChkSectionName
from .decoded_chk_section import DecodedChkSection


@dataclasses.dataclass(frozen=True)
class DecodedChk:
    _decoded_chk_sections: list[DecodedChkSection]

    @functools.cached_property
    def _sections_by_name(self) -> dict[ChkSectionName, list[DecodedChkSection]]:
        sections_by_name = defaultdict(list)
        for section in self._decoded_chk_sections:
            sections_by_name[section.section_name()].append(section)
        return sections_by_name

    @property
    def decoded_chk_sections(self) -> list[DecodedChkSection]:
        return deepcopy(self._decoded_chk_sections)

    def get_sections_by_name(
        self, chk_section_name: ChkSectionName
    ) -> list[DecodedChkSection]:
        return deepcopy(self._sections_by_name[chk_section_name])
