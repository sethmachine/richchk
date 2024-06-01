"""MRGN - Locations.  Data structure for a single location.

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

import dataclasses


@dataclasses.dataclass(frozen=True)
class DecodedLocation:
    """Represent a single decoded location from MRGN section.

    :param _left_x1: u32 left (X1) coordinate of location, in pixels (usually 32 pt grid
        aligned)
    :param _top_y1: u32 top (Y1) coordinate of location, in pixels
    :param _right_x2: u32 right (X2) coordinate of location, in pixels
    :param _bottom_y2: u32 bottom (Y2) coordinate of location, in pixels
    :param _string_id: u16 identifies the index of the string offset in the STR section
        for this location's name
    :param _elevation_flags: location elevation flags. If an elevation is disabled in
        the location, it's bit will be on (1) Bit 0 - Low elevation Bit 1 - Medium
        elevation Bit 2 - High elevation Bit 3 - Low air Bit 4 - Medium air Bit 5 - High
        air Bit 6-15 - Unused
    """

    _left_x1: int
    _top_y1: int
    _right_x2: int
    _bottom_y2: int
    _string_id: int
    _elevation_flags: int

    @property
    def left_x1(self) -> int:
        return self._left_x1

    @property
    def top_y1(self) -> int:
        return self._top_y1

    @property
    def right_x2(self) -> int:
        return self._right_x2

    @property
    def bottom_y2(self) -> int:
        return self._bottom_y2

    @property
    def string_id(self) -> int:
        return self._string_id

    @property
    def elevation_flags(self) -> int:
        return self._elevation_flags
