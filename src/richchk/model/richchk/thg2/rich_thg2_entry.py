"""THG2 - Sprites.  Rich data structure for a single sprite entry.

The rich representation drops the unused padding byte; it is hardcoded to 0 on encode.
"""

import dataclasses


@dataclasses.dataclass(frozen=True)
class RichSprite:
    """Represent a single rich sprite entry.

    :param _sprite_id: sprite type identifier
    :param _x: x coordinate
    :param _y: y coordinate
    :param _owner: owning player
    :param _flags: sprite flags
    """

    _sprite_id: int
    _x: int
    _y: int
    _owner: int
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
    def flags(self) -> int:
        return self._flags
