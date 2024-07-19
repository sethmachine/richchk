"""Searches an MPQ for files matching a pattern.

See: http://www.zezula.net/en/mpq/stormlib/sfilefindfirstfile.html
"""
import ctypes

from ...model.mpq.stormlib.search.stormlib_file_search_errors import (
    FailedToCloseSearchHandleException,
    NoFileFoundMatchingPatternException,
    NoMoreMatchingFilesFoundException,
)
from ...model.mpq.stormlib.search.stormlib_file_search_handle import (
    StormLibFileSearchHandle,
)
from ...model.mpq.stormlib.search.stormlib_file_search_operation_result import (
    StormLibFileSearchOperationResult,
)
from ...model.mpq.stormlib.search.stormlib_file_search_result import (
    StormLibFileSearchResult,
)
from ...model.mpq.stormlib.stormlib_operation import StormLibOperation
from ...model.mpq.stormlib.stormlib_operation_result import StormLibOperationResult
from ...model.mpq.stormlib.stormlib_reference import StormLibReference
from ...util import logger


class StormLibFileSearcher:
    def __init__(
        self,
        stormlib_reference: StormLibReference,
        open_mpq_handle: StormLibOperationResult,
    ) -> None:
        self._log = logger.get_logger(StormLibFileSearcher.__name__)
        self._open_mpq_handle = open_mpq_handle
        self._stormlib = stormlib_reference

    def find_all_files_matching_pattern(self, search_pattern: str) -> list[str]:
        """Finds all files in the MPQ archive matching the given pattern.

        Each element is the path the file is stored inside the MPQ archive, not the
        location of the file on disk.

        :param search_pattern: Name of the search mask. "*" will return all files.
        :return:
        """
        matching_filepaths = []
        try:
            file_search_wrapper = self._find_first_file_matching_pattern(search_pattern)
            matching_filepaths.append(
                file_search_wrapper.search_result.cFileName.decode("utf-8")
            )
            while True:
                try:
                    next_search_result = self._find_next_file(file_search_wrapper)
                    matching_filepaths.append(
                        next_search_result.search_result.cFileName.decode("utf-8")
                    )
                except NoMoreMatchingFilesFoundException:
                    break
            self._close_file_search(file_search_wrapper)
        except NoFileFoundMatchingPatternException:
            pass
        return matching_filepaths

    def _find_first_file_matching_pattern(
        self, search_pattern: str
    ) -> StormLibFileSearchOperationResult:
        """Find the first file matching a given pattern.

        Function SFileFindFirstFile searches an MPQ archive and returns name of the
        first file that matches the given search mask and exists in the MPQ archive.
        When the caller finishes searching, the returned handle must be freed by calling
        SFileFindClose.
        """
        search_result = StormLibFileSearchResult()
        self._stormlib.stormlib_dll.SFileFindFirstFile.restype = (
            StormLibFileSearchHandle
        )
        search_handle = self._stormlib.stormlib_dll.SFileFindFirstFile(
            self._open_mpq_handle.handle,
            search_pattern.encode("ascii"),
            ctypes.byref(search_result),
            None,
        )

        if (not search_handle) or (not search_result):
            raise NoFileFoundMatchingPatternException(
                f"No file was found matching the pattern: <{search_pattern}>.  "
                f"Try a different pattern instead "
                f"or the archive may not have the files you're looking for."
            )

        return StormLibFileSearchOperationResult(
            _search_handle=search_handle,
            _search_result=search_result,
        )

    def _find_next_file(
        self, stormlib_file_search_wrapper: StormLibFileSearchOperationResult
    ) -> StormLibFileSearchOperationResult:
        """Find the next file matching a given pattern.

        Function SFileFindNextFile continues search that has been initiated by
        SFileFindFirstFile. When the caller finishes searching, the returned handle must
        be freed by calling SFileFindClose.

        Return Value When the function succeeds, it returns nonzero and the
        SFILE_FIND_DATA structure is filled with information about the file. On an
        error, the function returns zero and GetLastError gives the error code.
        """
        search_result = StormLibFileSearchResult()
        func = getattr(
            self._stormlib.stormlib_dll, StormLibOperation.S_FILE_FIND_NEXT_FILE.value
        )
        result = func(
            stormlib_file_search_wrapper.search_handle,
            ctypes.byref(search_result),
        )
        if (not result) or (not search_result):
            raise NoMoreMatchingFilesFoundException(
                f"There are no more files matching the initial search pattern.  "
                f"Make sure the search handle is properly closed."
                f"Error code: {result}"
            )
        return StormLibFileSearchOperationResult(
            _search_handle=stormlib_file_search_wrapper.search_handle,
            _search_result=search_result,
        )

    def _close_file_search(
        self, stormlib_file_search_wrapper: StormLibFileSearchOperationResult
    ) -> None:
        """Function SFileFindClose closes a find handle that has been created by
        SFileFindFirstFile.

        Function SFileFindClose closes a find handle that has been created by
        SFileFindFirstFile.

        Parameters hFind [in] Search handle. Must have been obtained by call to
        SFileFindFirstFile. Return Value When the function succeeds, it returns nonzero.
        On an error, the function returns zero and GetLastError gives the error code.
        """
        func = getattr(
            self._stormlib.stormlib_dll, StormLibOperation.S_FILE_FIND_CLOSE.value
        )
        result = func(
            stormlib_file_search_wrapper.search_handle,
        )
        if not result:
            raise FailedToCloseSearchHandleException(
                f"Failed to close search handle.  Error code: {result}"
            )
