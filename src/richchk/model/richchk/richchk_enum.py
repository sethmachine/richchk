from enum import Enum
from typing import TypeVar

_T = TypeVar("_T", bound="RichChkEnum", covariant=True)


# TODO: make this an abstract class so it can't be instantiated directly
class RichChkEnum(Enum):
    def __init__(self, id_: int, name: str):
        self._id = id_
        self._name = name

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name
