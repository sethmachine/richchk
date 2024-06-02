"""Wraps StormLib DLL.

Avoid using this directly unless you know what you are doing.

For future compatibility, users of this wrapper should provide a path to their own
StormLib library compiled for their operating system and CPU architecture.
"""
import ctypes
import os

from ...model.mpq.stormlib.stormlib_archive_mode import StormLibArchiveMode
from ...model.mpq.stormlib.stormlib_operation_result import StormLibOperationResult
from ...model.mpq.stormlib.stormlib_reference import StormLibReference
from ...util import logger


class StormLibWrapper:
    def __init__(self, stormlib_reference: StormLibReference):
        self._log = logger.get_logger(StormLibWrapper.__name__)
        self._stormlib = stormlib_reference

    def open_archive(
        self, mpq_file_path: str, archive_mode: StormLibArchiveMode
    ) -> StormLibOperationResult:
        """Opens the MPQ archive, returning a pointer to its handle.

        The handle should be referenced in all future operations and the MPQ archive
        properly closed once done.
        """
        assert os.path.exists(mpq_file_path)
        operation = "SFileOpenArchive"
        handle = ctypes.c_void_p()
        func = getattr(self._stormlib.stormlib_dll, "SFileOpenArchive")
        result: int = func(
            mpq_file_path.encode("ascii"), 0, archive_mode.value, ctypes.byref(handle)
        )
        self._throw_if_archive_operation_fails(operation, result)
        return StormLibOperationResult(_handle=handle, _result=result)

    def close_archive(
        self, stormlib_operation_result: StormLibOperationResult
    ) -> StormLibOperationResult:
        """Closes an opened MPQ archive.

        :param stormlib_operation_result: the handle and result of a previous operation
            that opened the archive.
        :return:
        """
        operation = "SFileCloseArchive"
        func = getattr(self._stormlib.stormlib_dll, operation)
        result: int = func(stormlib_operation_result.handle)
        self._throw_if_archive_operation_fails(operation, result)
        return StormLibOperationResult(
            _handle=stormlib_operation_result.handle, _result=result
        )

    def _throw_if_archive_operation_fails(
        self, operation_name: str, result: int
    ) -> None:
        if result == 0:
            msg = (
                f"StormLib archive operation: <{operation_name}> failed due to a {result} result value.  "
                f"StormLib reference: {self._stormlib}"
            )
            self._log.error(msg)
            raise ValueError(msg)
