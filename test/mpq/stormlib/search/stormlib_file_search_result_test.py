import ctypes

import pytest

from richchk.model.mpq.stormlib.search.stormlib_file_search_result import (
    StormLibFileSearchResult,
)
from richchk.model.mpq.stormlib.stormlib_archive_mode import StormLibArchiveMode

from ....chk_resources import COMPLEX_STARCRAFT_SCX_MAP
from ....helpers.stormlib_test_helper import run_test_if_supported_os

_SENTINEL = 0xAA
_GUARD_BYTES = 4096


@pytest.mark.skipif(
    not run_test_if_supported_os(), reason="embedded StormLib not supported on this OS"
)
def test_find_data_struct_is_large_enough_for_stormlib(embedded_stormlib):
    """StormLib's SFILE_FIND_DATA uses MAX_PATH=1024 on macOS/Linux; a smaller Python
    struct lets StormLib write past its end and corrupt the heap."""
    dll = embedded_stormlib.stormlib.stormlib_dll
    dll.SFileFindFirstFile.restype = ctypes.c_void_p
    dll.SFileFindFirstFile.argtypes = [
        ctypes.c_void_p,
        ctypes.c_char_p,
        ctypes.c_void_p,
        ctypes.c_char_p,
    ]
    dll.SFileFindClose.argtypes = [ctypes.c_void_p]
    archive = embedded_stormlib.open_archive(
        str(COMPLEX_STARCRAFT_SCX_MAP), StormLibArchiveMode.STORMLIB_READ_ONLY
    )
    size = ctypes.sizeof(StormLibFileSearchResult)
    buf = (ctypes.c_ubyte * (size + _GUARD_BYTES))()
    ctypes.memset(buf, _SENTINEL, size + _GUARD_BYTES)
    search_handle = dll.SFileFindFirstFile(
        archive.handle, b"*", ctypes.addressof(buf), None
    )
    assert search_handle
    dll.SFileFindClose(search_handle)
    embedded_stormlib.close_archive(archive)
    written_past_struct = [b for b in bytes(buf)[size:] if b != _SENTINEL]
    assert written_past_struct == []
