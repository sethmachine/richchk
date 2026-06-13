"""A single terrain tile value from the MTXM or TILE section."""

import dataclasses


@dataclasses.dataclass(frozen=True)
class RichTile:
    """Represent a single terrain tile.

    :param _id: raw u16 tile value encoding a tile group index and subtile index
    """

    _id: int

    @property
    def id(self) -> int:
        return self._id

    @property
    def group_index(self) -> int:
        return (self._id >> 4) & 0x7FF

    @property
    def subtile_index(self) -> int:
        return self._id & 0xF
