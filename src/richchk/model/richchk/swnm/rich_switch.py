"""Represents a Switch that can be referenced in trigger data."""

import dataclasses
from typing import Any, Optional

from ..str.rich_string import RichNullString, RichString, is_rich_string_null_or_empty


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

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RichSwitch):
            if all([self.index is not None, other.index is not None]):
                return self.index == other.index
            else:
                if not all(
                    [
                        is_rich_string_null_or_empty(self.custom_name),
                        is_rich_string_null_or_empty(other.custom_name),
                    ]
                ):
                    return self.custom_name == other.custom_name
                return id(self) == id(other)
        return False

    def __hash__(self) -> int:
        # if the switch has not been allocated an index, there's no way to distinguish it from a
        # switch with the same exact values
        if self.index is None and is_rich_string_null_or_empty(self.custom_name):
            return hash(id(self))
        # Otherwise, use a hash based on the fields
        return hash(self._get_fields_for_equality())

    def _get_fields_for_equality(self) -> tuple[Any, ...]:
        return self._custom_name.value, self._index
