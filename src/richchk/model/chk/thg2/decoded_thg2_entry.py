"""THG2 - Sprites.  Data structure for a single sprite entry.

Each entry is 10 bytes: u16 sprite_id, u16 x, u16 y, u8 owner, u8 unused, u16 flags
"""

import dataclasses


@dataclasses.dataclass(frozen=True)
class DecodedThg2Entry:
    """Represent a single decoded sprite entry from the THG2 section.

    :param _sprite_id: u16 sprite type identifier
    :param _x: u16 x coordinate
    :param _y: u16 y coordinate
    :param _owner: u8 owning player
    :param _unused: u8 unused padding byte
    :param _flags: u16 sprite flags
    """

    _sprite_id: int
    _x: int
    _y: int
    _owner: int
    _unused: int
    _flags: int

    @property
    def sprite_id(self) -> int:
        return self._sprite_id

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
    def unused(self) -> int:
        return self._unused

    @property
    def flags(self) -> int:
        return self._flags
