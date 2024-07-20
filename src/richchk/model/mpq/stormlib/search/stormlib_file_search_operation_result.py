"""The result of using a StormLib SFileFindFirstFile or SFileFindNextFile."""
import dataclasses

from .stormlib_file_search_handle import StormLibFileSearchHandle
from .stormlib_file_search_result import StormLibFileSearchResult


@dataclasses.dataclass(frozen=True)
class StormLibFileSearchOperationResult:
    _search_handle: StormLibFileSearchHandle
    _search_result: StormLibFileSearchResult

    @property
    def search_handle(self) -> StormLibFileSearchHandle:
        return self._search_handle

    @property
    def search_result(self) -> StormLibFileSearchResult:
        return self._search_result
