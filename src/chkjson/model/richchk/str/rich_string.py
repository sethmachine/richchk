"""Represents a string that needs to be encoded into the DecodedStrSection."""

import dataclasses


@dataclasses.dataclass(frozen=True)
class RichString:
    _value: str

    @property
    def value(self) -> str:
        return self._value
