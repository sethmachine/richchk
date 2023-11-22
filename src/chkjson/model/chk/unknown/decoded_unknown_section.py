"""Handler for unknown CHK sections.

UNKNOWN is not an actual CHK section name.
This is just convenience to allow handling partially decoded CHK files.
"""

import dataclasses

from chkjson.model.chk.decoded_chk_section import DecodedChkSection
from chkjson.model.chk_section_name import ChkSectionName


@dataclasses.dataclass(frozen=True)
class DecodedUnknownSection(DecodedChkSection):
    _actual_section_name: str
    _chk_binary_data: bytes

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.UNKNOWN

    @property
    def actual_section_name(self) -> str:
        return self._actual_section_name

    @property
    def chk_binary_data(self) -> bytes:
        return self._chk_binary_data
