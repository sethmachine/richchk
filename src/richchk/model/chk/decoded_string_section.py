"""Provide a common interface for using both STR and STRx."""
from typing import Protocol


class DecodedStringSection(Protocol):
    @property
    def number_of_strings(self) -> int:
        raise NotImplementedError

    @property
    def strings_offsets(self) -> list[int]:
        raise NotImplementedError

    @property
    def strings(self) -> list[str]:
        raise NotImplementedError
