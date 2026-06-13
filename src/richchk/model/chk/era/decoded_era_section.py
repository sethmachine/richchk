"""ERA - Tileset.

Required for all versions and all game types. Validation: Must be size of 2 bytes.

This section identifies the tileset of the scenario.

u16: Tileset index (0-7):

0 - Badlands

1 - Space Platform

2 - Installation

3 - Ashworld

4 - Jungle

5 - Desert

6 - Ice

7 - Twilight
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..decoded_chk_section import DecodedChkSection


@dataclasses.dataclass(frozen=True)
class DecodedEraSection(DecodedChkSection):
    """Represent ERA - Tileset.

    :param _tileset: u16 tileset index
    """

    _tileset: int

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.ERA

    @property
    def tileset(self) -> int:
        return self._tileset
