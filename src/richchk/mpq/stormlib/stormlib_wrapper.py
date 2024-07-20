"""Wraps StormLib DLL.

Avoid using this directly unless you know what you are doing.

For future compatibility, users of this wrapper should provide a path to their own
StormLib library compiled for their operating system and CPU architecture.
"""
import ctypes
import os

from ...model.mpq.stormlib.stormlib_archive_mode import StormLibArchiveMode
from ...model.mpq.stormlib.stormlib_flag import StormLibFlag
from ...model.mpq.stormlib.stormlib_mpq_handle import StormLibMpqHandle
from ...model.mpq.stormlib.stormlib_operation import StormLibOperation
from ...model.mpq.stormlib.stormlib_operation_result import StormLibOperationResult
from ...model.mpq.stormlib.stormlib_reference import StormLibReference
from ...util import logger


class StormLibWrapper:
    def __init__(self, stormlib_reference: StormLibReference):
        self._log = logger.get_logger(StormLibWrapper.__name__)
        self._stormlib = stormlib_reference

    @property
    def stormlib(self) -> StormLibReference:
        return self._stormlib

    def open_archive(
        self, mpq_file_path: str, archive_mode: StormLibArchiveMode
    ) -> StormLibOperationResult:
        """Opens the MPQ archive, returning a pointer to its handle.

        For Starcraft, this will generally be .SCX or .SCM file.  For Warcraft 3, it
        will be a .W3M or W3X.

        The handle should be referenced in all future operations and the MPQ archive
        properly closed once done.
        """
        assert os.path.exists(mpq_file_path)
        handle = StormLibMpqHandle()
        func = getattr(
            self._stormlib.stormlib_dll, StormLibOperation.S_FILE_OPEN_ARCHIVE.value
        )
        result: int = func(
            mpq_file_path.encode("ascii"), 0, archive_mode.value, ctypes.byref(handle)
        )
        self._throw_if_operation_fails(
            StormLibOperation.S_FILE_OPEN_ARCHIVE.value, result
        )
        return StormLibOperationResult(_handle=handle, _result=result)

    def close_archive(
        self, stormlib_operation_result: StormLibOperationResult
    ) -> StormLibOperationResult:
        """Closes an opened MPQ archive.

        :param stormlib_operation_result: the handle and result of a previous operation
            that opened the archive.
        :return:
        """
        func = getattr(
            self._stormlib.stormlib_dll, StormLibOperation.S_FILE_CLOSE_ARCHIVE.value
        )
        result: int = func(stormlib_operation_result.handle)
        self._throw_if_operation_fails(
            StormLibOperation.S_FILE_CLOSE_ARCHIVE.value, result
        )
        return StormLibOperationResult(
            _handle=stormlib_operation_result.handle, _result=result
        )

    def extract_file(
        self,
        stormlib_operation_result: StormLibOperationResult,
        path_to_file_in_archive: str,
        outfile: str,
        overwrite_existing: bool = False,
    ) -> StormLibOperationResult:
        """Extracts a file to the destination path from the opened MPQ archive.

        :param stormlib_operation_result:
        :param path_to_file_in_archive:
        :param outfile:
        :param overwrite_existing:
        :return:
        """
        if os.path.exists(outfile) and not overwrite_existing:
            msg = (
                f"Refusing to extract {path_to_file_in_archive} "
                f"because the output file {outfile} already exists."
            )
            self._log.error(msg)
            raise FileExistsError(msg)
        func = getattr(
            self._stormlib.stormlib_dll, StormLibOperation.S_FILE_EXTRACT_FILE.value
        )
        result: int = func(
            stormlib_operation_result.handle,
            path_to_file_in_archive.encode("ascii"),
            outfile.encode("ascii"),
            StormLibFlag.SFILE_OPEN_FROM_MPQ.value,
        )
        self._throw_if_operation_fails(
            StormLibOperation.S_FILE_EXTRACT_FILE.value, result
        )
        return StormLibOperationResult(
            _handle=stormlib_operation_result.handle, _result=result
        )

    def add_file(
        self,
        stormlib_operation_result: StormLibOperationResult,
        infile: str,
        path_to_file_in_archive: str,
        overwrite_existing: bool = False,
    ) -> StormLibOperationResult:
        """Add a local file to the archive with the given name.

        Note when adding a new file name to the archive that did not exist before, the
        list file must be updated with the new file in order to allow compaction of the
        archive to succeed.

        :param stormlib_operation_result:
        :param infile:
        :param path_to_file_in_archive:
        :param overwrite_existing:
        :return:
        """
        assert os.path.exists(infile)
        flags = StormLibFlag.MPQ_FILE_COMPRESS.value
        if overwrite_existing:
            flags += StormLibFlag.MPQ_FILE_REPLACEEXISTING.value
        compression = StormLibFlag.MPQ_COMPRESSION_ZLIB.value
        func = getattr(
            self._stormlib.stormlib_dll, StormLibOperation.S_FILE_ADD_FILE.value
        )
        result: int = func(
            stormlib_operation_result.handle,
            infile.encode("ascii"),
            path_to_file_in_archive.encode("ascii"),
            flags,
            compression,
            compression,
        )
        self._throw_if_operation_fails(StormLibOperation.S_FILE_ADD_FILE.value, result)
        return StormLibOperationResult(
            _handle=stormlib_operation_result.handle, _result=result
        )

    def compact_archive(
        self, stormlib_operation_result: StormLibOperationResult
    ) -> StormLibOperationResult:
        """Compact an archive open in write mode with no listfile.

        :param stormlib_operation_result:
        :return:
        """
        func = getattr(
            self._stormlib.stormlib_dll, StormLibOperation.S_FILE_COMPACT_ARCHIVE.value
        )
        result: int = func(stormlib_operation_result.handle, None, 0)
        self._throw_if_operation_fails(
            StormLibOperation.S_FILE_COMPACT_ARCHIVE.value, result
        )
        return StormLibOperationResult(
            _handle=stormlib_operation_result.handle, _result=result
        )

    def _throw_if_operation_fails(self, operation_name: str, result: int) -> None:
        if result == 0:
            msg = (
                f"StormLib archive operation: <{operation_name}> failed due to a {result} result value.  "
                f"StormLib reference: {self._stormlib}"
            )
            self._log.error(msg)
            raise ValueError(msg)
