"""Represents a string that needs to be encoded into the DecodedStrSection."""

import dataclasses


@dataclasses.dataclass(frozen=True)
class RichString:
    _value: str

    @property
    def value(self) -> str:
        return self._value


@dataclasses.dataclass(frozen=True)
class RichNullString(RichString):
    """Indicates the absence of a non-default string name."""

    _value: str = ""

    def __post_init__(self) -> None:
        if self._value:
            raise ValueError(
                "RichNullString can only have empty string values.  "
                "Do not use this class to store custom string data."
            )
