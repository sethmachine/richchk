"""Determines which StormLib DLL to use based on operating system and CPU architecture.

For future compatibility, users of this wrapper should provide a path to their own
StormLib library compiled for their operating system and CPU architecture.
"""

import os
import platform
from typing import Optional

from ...model.mpq.stormlib.stormlib_file_path import StormLibFilePath
from ...util import logger


class StormLibFinder:
    _LOG = logger.get_logger("StormLibFinder")
    _SCRIPT_PATH = os.path.dirname(__file__)
    _MAC_STORM_INTEL = os.path.join(_SCRIPT_PATH, "dlls/macos/libStorm.dylib")
    _MAC_STORM_M1 = os.path.join(_SCRIPT_PATH, "dlls/macos/libstorm.9.22.0.dylib")
    _WINDOWS_STORM = os.path.join(_SCRIPT_PATH, "dlls/windows/Storm.dll")
    _LINUX_STORM_X86_64 = os.path.join(_SCRIPT_PATH, "dlls/linux/libstorm.so.9.22.0")

    @classmethod
    def find_stormlib(
        cls, path_to_stormlib_dll: Optional[str] = None
    ) -> StormLibFilePath:
        if path_to_stormlib_dll:
            assert os.path.exists(path_to_stormlib_dll)
            return StormLibFilePath(_path_to_stormlib_dll=path_to_stormlib_dll)
        else:
            cls._LOG.warning(
                "No path to a StormLib DLL was provided, "
                "attempting to use precompiled DLL for Windows, macOS and Linux. "
                "Future compatibility is not guaranteed; "
                "please provide a path to StormLib DLL compiled for your platform."
            )
            if platform.system().lower() == "windows":
                return StormLibFilePath(_path_to_stormlib_dll=cls._WINDOWS_STORM)
            elif (
                platform.system().lower() == "darwin"
                and platform.machine().lower() == "arm64"
            ):
                return StormLibFilePath(_path_to_stormlib_dll=cls._MAC_STORM_M1)
            elif platform.system().lower() == "darwin":
                return StormLibFilePath(_path_to_stormlib_dll=cls._MAC_STORM_INTEL)
            elif (
                platform.system().lower() == "linux"
                and platform.machine().lower() == "x86_64"
            ):
                return StormLibFilePath(_path_to_stormlib_dll=cls._LINUX_STORM_X86_64)
            else:
                msg = (
                    f"Unsupported platform for precompiled StormLib DLL.  "
                    f"Provide a path to a StormLib DLL compiled for your system: {platform.system()}"
                )
                cls._LOG.error(msg)
                raise OSError(msg)
