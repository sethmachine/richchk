"""DD2 - Doodads.  Rich data structure for a single doodad entry.

The rich representation converts the enabled field from int to bool.
"""

import dataclasses


@dataclasses.dataclass(frozen=True)
class RichDoodad:
    """Represent a single rich doodad entry.

    :param _doodad_id: doodad type identifier
    :param _x: x coordinate
    :param _y: y coordinate
    :param _owner: owning player
    :param _enabled: whether the doodad is enabled
    """

    _doodad_id: int
    _x: int
    _y: int
    _owner: int
    _enabled: bool

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
    def enabled(self) -> bool:
        return self._enabled
