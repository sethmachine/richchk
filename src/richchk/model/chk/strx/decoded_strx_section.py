""" "STRx" - String Data.

Required for all versions and all game types (or STR) Validation: Must be at least 1
byte (assumed, not confirmed).

Note, the STR section can also exist and optionally replace the STRx section.

Note, the encoding of text in the STRx section is unspecified. Commonly it is UTF-8 but
anything is possible.

The STRx section is a simple bit extension to the STR section introduced in StarCraft
Remastered.

This section contains all the strings in the map.

u32: Number of strings in the section (Default: 1024)

u32[Number of strings]: 1 integer for each string specifying the offset (the spot where
the string starts in the section from the start of it).

Strings: After the offsets, this is where every string in the map goes, one after
another. Each one is terminated by a null character.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..decoded_chk_section import DecodedChkSection
from ..decoded_string_section import DecodedStringSection


@dataclasses.dataclass(frozen=True)
class DecodedStrxSection(DecodedChkSection, DecodedStringSection):
    # u32: Number of strings in the section (Default: 1024)
    _number_of_strings: int
    # u32[Number of strings]: 1 integer for each string specifying the offset
    # (the spot where the string starts in the section from the start of it).
    _string_offsets: list[int]
    # Strings: After the offsets, this is where every string in the map goes,
    # one after another. Each one is terminated by a null character.
    _strings: list[str]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.STRX

    @property
    def number_of_strings(self) -> int:
        return self._number_of_strings

    @property
    def strings_offsets(self) -> list[int]:
        return self._string_offsets

    @property
    def strings(self) -> list[str]:
        return self._strings
