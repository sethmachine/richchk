"""Provide a convenient way to get a StormLibWrapper object for MPQ/RichChk IO."""
from typing import Optional

from ...mpq.stormlib.stormlib_wrapper import StormLibWrapper
from .stormlib_finder import StormLibFinder
from .stormlib_loader import StormLibLoader


class StormLibHelper:
    @staticmethod
    def load_stormlib(path_to_stormlib_dll: Optional[str] = None) -> StormLibWrapper:
        """Load StormLib DLL into a wrapper for usage.

        :param path_to_stormlib_dll: path to the DLL on the local machine. If not
            provided, will attempt to use an embedded DLL in RichChk.
        :return:
        """
        stormlib_path = StormLibFinder.find_stormlib(
            path_to_stormlib_dll=path_to_stormlib_dll
        )
        stormlib = StormLibLoader.load_stormlib(stormlib_path)
        return StormLibWrapper(stormlib)
