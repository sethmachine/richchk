"""Represents a WAV file that can be referenced in trigger data."""

import dataclasses

from ..str.rich_string import RichString


@dataclasses.dataclass(frozen=True)
class RichWav:
    _path_in_chk: RichString
    _index: int

    @property
    def path_in_chk(self) -> RichString:
        return self._path_in_chk

    @property
    def index(self) -> int:
        return self._index
