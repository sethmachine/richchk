"""Represents a Switch that can be referenced in trigger data."""

import dataclasses
from typing import Optional

from ..str.rich_string import RichNullString, RichString


@dataclasses.dataclass(frozen=True)
class RichSwitch:
    _custom_name: RichString = RichNullString()
    _index: Optional[int] = None

    @property
    def custom_name(self) -> RichString:
        return self._custom_name

    @property
    def index(self) -> Optional[int]:
        return self._index
