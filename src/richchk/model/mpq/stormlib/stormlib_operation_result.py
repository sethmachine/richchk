"""The result of using a StormLib function each time.

A zero result code indicates an error.
"""
import ctypes
import dataclasses


@dataclasses.dataclass(frozen=True)
class StormLibOperationResult:
    _handle: ctypes.c_void_p
    _result: int

    @property
    def handle(self) -> ctypes.c_void_p:
        return self._handle

    @property
    def result(self) -> int:
        return self._result
