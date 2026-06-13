"""DD2 - Doodads.  Data structure for a single doodad entry.

Each entry is 8 bytes: u16 doodad_id, u16 x, u16 y, u8 owner, u8 enabled
"""

import dataclasses


@dataclasses.dataclass(frozen=True)
class DecodedDd2Entry:
    """Represent a single decoded doodad entry from the DD2 section.

    :param _doodad_id: u16 doodad type identifier
    :param _x: u16 x coordinate
    :param _y: u16 y coordinate
    :param _owner: u8 owning player
    :param _enabled: u8 whether the doodad is enabled (0 or 1)
    """

    _doodad_id: int
    _x: int
    _y: int
    _owner: int
    _enabled: int

    @property
    def doodad_id(self) -> int:
        return self._doodad_id

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def owner(self) -> int:
        return self._owner

    @property
    def enabled(self) -> int:
        return self._enabled
