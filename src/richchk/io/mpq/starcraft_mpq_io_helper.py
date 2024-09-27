"""Convenient method to create a StarcraftMpqIo from a path to StormLib DLL."""
from typing import Optional

from ...mpq.stormlib.stormlib_helper import StormLibHelper
from .starcraft_mpq_io import StarcraftMpqIo


class StarcraftMpqIoHelper:
    @staticmethod
    def create_starcraft_mpqio(
        path_to_stormlib_dll: Optional[str] = None,
    ) -> StarcraftMpqIo:
        """Create a StarcraftMpqIo from a path to StormLib DLL.

        :param path_to_stormlib_dll: path to the DLL on the local machine. If not
            provided, will attempt to use an embedded DLL in RichChk.
        :return:
        """
        return StarcraftMpqIo(
            stormlib_wrapper=StormLibHelper.load_stormlib(path_to_stormlib_dll)
        )
