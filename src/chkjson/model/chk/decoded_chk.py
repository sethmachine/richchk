"""Represents the ordered list of decoded CHK sections from a decoded CHK file.

"""

from copy import deepcopy
from dataclasses import dataclass

from .decoded_chk_section import DecodedChkSection


@dataclass(frozen=True)
class DecodedChk:
    _decoded_chk_sections: list[DecodedChkSection]

    @property
    def decoded_chk_sections(self) -> list[DecodedChkSection]:
        return deepcopy(self._decoded_chk_sections)
