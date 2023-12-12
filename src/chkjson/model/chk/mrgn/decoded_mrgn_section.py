"""MRGN - Locations.

Required for all versions. Not required for Melee. Validation: 1280 bytes for retail,
5100 bytes for Hybrid and Broodwar.

This section contains all the locations that the map uses. In a vanilla map, this
section contains 64 locations. In a Hybrid or Brood War map, this section will expand to
contain 255 locations.

Each location gets one of the following location entries. The 'Anywhere' location, is
ALWAYS location 64.

u32: Left (X1) coordinate of location, in pixels (usually 32 pt grid aligned)

u32: Top (Y1) coordinate of location, in pixels

u32: Right (X2) coordinate of location, in pixels

u32: Bottom (Y2) coordinate of location, in pixels

u16: String number of the name of this location

u16: Location elevation flags. If an elevation is disabled in the location, it's bit
will be on (1)

Bit 0 - Low elevation

Bit 1 - Medium elevation

Bit 2 - High elevation

Bit 3 - Low air

Bit 4 - Medium air

Bit 5 - High air

Bit 6-15 - Unused

Note that in typical locations Right is always larger than Left and Bottom is always
larger than Top. However, you can reverse one or both of these for Inverted Locations.
"""

import copy
import dataclasses

from ...chk_section_name import ChkSectionName
from ..decoded_chk_section import DecodedChkSection
from .decoded_location import DecodedLocation


@dataclasses.dataclass(frozen=True)
class DecodedMrgnSection(DecodedChkSection):
    """Represent MRGN section for all location data in a map.

    :param _locations: In a vanilla map, this section contains 64 locations. In a Hybrid
        or Brood War map, this section will expand to contain 255 locations
    """

    # This section contains all the locations that the map uses.
    # In a vanilla map, this section contains 64 locations.
    # In a Hybrid or Brood War map, this section will expand to contain 255 locations.
    _locations: list[DecodedLocation]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.MRGN

    @property
    def locations(self) -> list[DecodedLocation]:
        return copy.deepcopy(self._locations)
