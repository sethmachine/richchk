"""Reference to absolute file path location of the StormLib DLL."""

import dataclasses
from ctypes import CDLL

from .stormlib_file_path import StormLibFilePath


@dataclasses.dataclass(frozen=True)
class StormLibReference:
    _path_to_stormlib: StormLibFilePath
    _stormlib_dll: CDLL

    @property
    def path_to_stormlib(self) -> StormLibFilePath:
        return self._path_to_stormlib

    @property
    def stormlib_dll(self) -> CDLL:
        return self._stormlib_dll
