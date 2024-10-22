"""Wraps StormLib DLL.

Avoid using this directly unless you know what you are doing.

For future compatibility, users of this wrapper should provide a path to their own
StormLib library compiled for their operating system and CPU architecture.
"""
import ctypes
import os
import platform
from ctypes import POINTER
from typing import Any, Union

from ...model.mpq.stormlib.stormlib_archive_mode import StormLibArchiveMode
from ...model.mpq.stormlib.stormlib_flag import StormLibFlag
from ...model.mpq.stormlib.stormlib_mpq_handle import StormLibMpqHandle
from ...model.mpq.stormlib.stormlib_operation import StormLibOperation
from ...model.mpq.stormlib.stormlib_operation_result import StormLibOperationResult
from ...model.mpq.stormlib.stormlib_reference import StormLibReference
from ...util import logger

_STORMLIB_STRING_ARG_ENCODING = "ascii"


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
        func.restype = ctypes.c_bool
        func.argtypes = self._get_arg_types_for_open_archive_for_platform()
        result: int = func(
            self._encode_file_path_for_platform(mpq_file_path),
            0,
            archive_mode.value,
            ctypes.byref(handle),
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
        func.argtypes = [StormLibMpqHandle]
        result = func(stormlib_operation_result.handle)
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
            self._encode_file_path_for_platform(outfile),
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

        Some protected files cannot be modified this way:

        https://github.com/ladislav-zezula/StormLib/blob/539a04e06578ce9b0cf005446eff66e18753076d/doc/History.txt#L44-L48

        ("(listfile)", "(attributes)" and "(signature)")

        :param stormlib_operation_result:
        :param infile:
        :param path_to_file_in_archive:
        :param overwrite_existing:
        :return:
        """
        assert os.path.exists(infile)
        self._log.info(f"adding files: {infile} to {path_to_file_in_archive}")
        flags = StormLibFlag.MPQ_FILE_COMPRESS.value
        if overwrite_existing:
            flags += StormLibFlag.MPQ_FILE_REPLACEEXISTING.value
        compression = StormLibFlag.MPQ_COMPRESSION_ZLIB.value
        func = getattr(
            self._stormlib.stormlib_dll, StormLibOperation.S_FILE_ADD_FILE_EX.value
        )
        result: int = func(
            stormlib_operation_result.handle,
            self._encode_file_path_for_platform(infile),
            path_to_file_in_archive.encode("ascii"),
            flags,
            compression,
            compression,
        )
        self._throw_if_operation_fails(
            StormLibOperation.S_FILE_ADD_FILE_EX.value, result
        )
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

    def _get_arg_types_for_open_archive_for_platform(self) -> list[Any]:
        """Return argument types for opening an archive based on OS.

        Unsure why Windows uses different signatures than Linux/macOS.  Maybe it depends
        upon how the Windows StormLib was compiled?

        :return:
        """
        if platform.system().lower() == "windows":
            return [
                ctypes.c_wchar_p,
                ctypes.c_uint,
                ctypes.c_uint,
                POINTER(StormLibMpqHandle),
            ]
        return [
            ctypes.c_char_p,
            ctypes.c_uint,
            ctypes.c_uint,
            POINTER(StormLibMpqHandle),
        ]

    def _encode_file_path_for_platform(
        self, path_to_file_on_disk: str
    ) -> Union[str, bytes]:
        """Create the file path string encoding needed for StormLib arguments depending
        upon OS.

        :param path_to_file_on_disk: the string path to a file on disk (not in the MPQ
            archive)
        :return:
        """
        if platform.system().lower() == "windows":
            return path_to_file_on_disk
        return path_to_file_on_disk.encode(_STORMLIB_STRING_ARG_ENCODING)

    def _throw_if_operation_fails(self, operation_name: str, result: int) -> None:
        if result == 0:
            func = getattr(self._stormlib.stormlib_dll, "GetLastError")
            func.restype = ctypes.c_uint
            getLastErrorCode = func()
            msg = (
                f"StormLib archive operation: <{operation_name}> failed due to a {result} result value.  "
                f"Error code: {getLastErrorCode}, "
                f"StormLib reference: {self._stormlib}"
            )
            self._log.error(msg)
            raise ValueError(msg)
