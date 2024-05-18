from enum import Enum
from typing import TypeVar

_T = TypeVar("_T", bound="RichChkEnum", covariant=True)


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

    @classmethod
    def get_by_id(cls, id_: int) -> "RichChkEnum":
        return {e.id: e for e in cls}[id_]

    @classmethod
    def contains(cls, id_: int) -> bool:
        return id_ in {e.id: e for e in cls}
