"""A player or group ID beyond the named PlayerId values.

The player/group argument of a trigger action or condition is a u32.  StarCraft only
names the values 0 to 26 (see PlayerId), but real maps store other values there, and
Deaths conditions and actions use huge ones to read and write memory outside the death
count table (EUDs).  Such a value is decoded as an _ExtendedPlayerId so it is preserved
exactly when the map is written back.

This is deliberately private: use PlayerId for every named player.  Trigger arguments
are typed AnyPlayerId, which is PlayerId or _ExtendedPlayerId.
"""

import dataclasses
import typing
from typing import Union

from ....util import logger
from .player_id import PlayerId

__all__ = ["AnyPlayerId"]

_MAX_PLAYER_ID = 0xFFFFFFFF
_NAMED_PLAYER_IDS = {player_id.id: player_id for player_id in PlayerId}
_LOG = logger.get_logger("ExtendedPlayerId")


@typing.final
@dataclasses.dataclass(frozen=True)
class _ExtendedPlayerId:
    _value: int

    def __post_init__(self) -> None:
        if self._value in _NAMED_PLAYER_IDS:
            msg = (
                f"{self._value} is a named player ID.  "
                f"Use {_NAMED_PLAYER_IDS[self._value]} instead."
            )
            _LOG.error(msg)
            raise ValueError(msg)
        if not 0 <= self._value <= _MAX_PLAYER_ID:
            msg = (
                f"Extended player ID {self._value} is out of range.  "
                f"A player ID is stored as a u32 and cannot exceed {_MAX_PLAYER_ID}."
            )
            _LOG.error(msg)
            raise ValueError(msg)

    @property
    def id(self) -> int:
        return self._value


AnyPlayerId = Union[PlayerId, _ExtendedPlayerId]
