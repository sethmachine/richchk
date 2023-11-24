""""STR " - String Data

Required for all versions and all game types (or STRx).
Validation: Must be at least 1 byte.

Note, since StarCraft Remastered, the "STRx" section is also possible and it optionally replaces the STR section.

Note, the encoding of text in the STR section is unspecified. Common encodings are CP-1252, CP-949, and later, UTF-8,
(but anything is possible)

This section contains all the strings in the map.

u16: Number of strings in the section (Default: 1024)
u16[Number of strings]: 1 integer for each string specifying the offset (the spot where the string starts
in the section from the start of it).
Strings: After the offsets, this is where every string in the map goes, one after another. Each one is terminated
by a null character.
This section can contain more or less then 1024 string offsests and will work in Starcraft.
By default the first byte in Strings is a NUL character, and all unused offsets in the STR section point
to this NUL character. Note that STR sections can be stacked in a similar fashion as MTXM

"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..decoded_chk_section import DecodedChkSection


@dataclasses.dataclass(frozen=True)
class DecodedStrSection(DecodedChkSection):
    # u16: Number of strings in the section (Default: 1024)
    _number_of_strings: int
    # u16[Number of strings]: 1 integer for each string specifying the offset
    # (the spot where the string starts in the section from the start of it).
    _strings_offset: list[int]
    # Strings: After the offsets, this is where every string in the map goes, one after another.
    # Each one is terminated by a null character.
    _strings: list[str]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.STR

    @property
    def number_of_strings_u16(self) -> int:
        return self._number_of_strings

    @property
    def strings_offset_u16(self) -> list[int]:
        return self._strings_offset.copy()

    @property
    def strings(self) -> list[str]:
        return self._strings.copy()
