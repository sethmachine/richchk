"""The result of using a StormLib function each time.

A zero result code indicates an error.
"""
import dataclasses

from richchk.model.mpq.stormlib.stormlib_mpq_handle import StormLibMpqHandle


@dataclasses.dataclass(frozen=True)
class StormLibOperationResult:
    _handle: StormLibMpqHandle
    _result: int

    @property
    def handle(self) -> StormLibMpqHandle:
        return self._handle

    @property
    def result(self) -> int:
        return self._result
