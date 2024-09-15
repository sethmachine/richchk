"""Represents the instance of a single location found in the MRGN section.

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
from typing import Any, Optional

from ..str.rich_string import RichString


@dataclasses.dataclass(frozen=True)
class RichLocation:
    _left_x1: int
    _top_y1: int
    _right_x2: int
    _bottom_y2: int
    _custom_location_name: RichString
    _index: Optional[int] = None
    _low_elevation: bool = True
    _medium_elevation: bool = True
    _high_elevation: bool = True
    _low_air: bool = True
    _medium_air: bool = True
    _high_air: bool = True

    def __eq__(self, other: object) -> bool:
        # 2 locations are only equal if they both have been allocated an index in the MRGN
        # and all their fields match
        # if a location does not have an index allocated, only the exact same objects in memory can be equal
        if isinstance(other, RichLocation):
            if self._index is not None and other._index is not None:
                return (
                    self._get_fields_for_equality() == other._get_fields_for_equality()
                )
            elif any([self._index is None, other.index is None]):
                return (
                    self._get_fields_for_equality_missing_index()
                    == other._get_fields_for_equality_missing_index()
                )
            else:
                return id(self) == id(other)
        return False

    def __hash__(self) -> int:
        # if the location has not been allocated an index, there's no way to distinguish it from a
        # location with the same exact values
        # if self._index is None:
        #     return hash(id(self))
        # Otherwise, use a hash based on the fields x and y
        return hash(self._get_fields_for_equality())

    def _get_fields_for_equality(self) -> tuple[Any, ...]:
        return (
            self._left_x1,
            self.top_y1,
            self._right_x2,
            self._bottom_y2,
            self._custom_location_name,
            self._index,
            self._low_elevation,
            self._medium_elevation,
            self._high_elevation,
            self._low_air,
            self._medium_air,
            self._high_air,
        )

    def _get_fields_for_equality_missing_index(self) -> tuple[Any, ...]:
        return (
            self._left_x1,
            self.top_y1,
            self._right_x2,
            self._bottom_y2,
            self._custom_location_name,
            self._low_elevation,
            self._medium_elevation,
            self._high_elevation,
            self._low_air,
            self._medium_air,
            self._high_air,
        )

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
    def custom_location_name(self) -> RichString:
        return self._custom_location_name

    @property
    def index(self) -> Optional[int]:
        return self._index

    @property
    def low_elevation(self) -> bool:
        return self._low_elevation

    @property
    def medium_elevation(self) -> bool:
        return self._medium_elevation

    @property
    def high_elevation(self) -> bool:
        return self._high_elevation

    @property
    def low_air(self) -> bool:
        return self._low_air

    @property
    def medium_air(self) -> bool:
        return self._medium_air

    @property
    def high_air(self) -> bool:
        return self._high_air
