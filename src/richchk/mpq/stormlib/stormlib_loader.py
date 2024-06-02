"""Loads StormLib DLL.

Avoid using this directly unless you know what you are doing.

For future compatibility, users of this wrapper should provide a path to their own
StormLib library compiled for their operating system and CPU architecture.
"""
import ctypes

from ...model.mpq.stormlib.stormlib_file_path import StormLibFilePath
from ...model.mpq.stormlib.stormlib_reference import StormLibReference
from ...util import logger


class StormLibLoader:
    _LOG = logger.get_logger("StormLibLoader")

    @classmethod
    def load_stormlib(cls, path_to_stormlib: StormLibFilePath) -> StormLibReference:
        return StormLibReference(
            _path_to_stormlib=path_to_stormlib,
            _stormlib_dll=ctypes.cdll.LoadLibrary(
                path_to_stormlib.path_to_stormlib_dll
            ),
        )
