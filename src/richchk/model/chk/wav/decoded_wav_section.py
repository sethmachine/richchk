""" "WAV " - WAV String Indexes.

Not Required.

There are 512 wav entires regardless of how many are actually used.

u32[512]: 1 long for each WAV. Indicates a string index is used for a WAV path in the
MPQ. If the entry is not used, it will be 0.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..decoded_chk_section import DecodedChkSection


@dataclasses.dataclass(frozen=True)
class DecodedWavSection(DecodedChkSection):
    """Represent WAV - WAV string indices.

    :param _wav_string_ids: 1 long for each WAV. Indicates a string index is used for a
        WAV path in the MPQ. If the entry is not used, it will be 0.
    """

    _wav_string_ids: list[int]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.WAV

    @property
    def wav_string_ids(self) -> list[int]:
        return self._wav_string_ids
