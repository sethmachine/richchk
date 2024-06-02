from enum import Enum

from richchk.model.mpq.stormlib.stormlib_flag import StormLibFlag


class StormLibArchiveMode(Enum):
    STORMLIB_READ_ONLY = (StormLibFlag.STREAM_FLAG_READ_ONLY.value,)
    STORMLIB_WRITE_ONLY = (StormLibFlag.STREAM_FLAG_WRITE_SHARE.value,)

    def __init__(self, value: int):
        self._value = value

    @property
    def value(self) -> int:
        return self._value
