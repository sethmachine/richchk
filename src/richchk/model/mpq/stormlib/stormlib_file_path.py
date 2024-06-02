"""Reference to absolute file path location of the StormLib DLL."""

import dataclasses


@dataclasses.dataclass(frozen=True)
class StormLibFilePath:
    _path_to_stormlib_dll: str

    @property
    def path_to_stormlib_dll(self) -> str:
        return self._path_to_stormlib_dll
