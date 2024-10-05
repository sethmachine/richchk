"""Convenient method to create a StarcraftMpqIo from a path to StormLib DLL."""
from typing import Optional

from ...mpq.stormlib.stormlib_helper import StormLibHelper
from .starcraft_mpq_io import StarCraftMpqIo
from .starcraft_wav_io import StarCraftWavIo
from .starcraft_wav_metadata_io import StarCraftWavMetadataIo


class StarCraftMpqIoHelper:
    @staticmethod
    def create_mpq_io(
        path_to_stormlib_dll: Optional[str] = None,
    ) -> StarCraftMpqIo:
        """Create a StarcraftMpqIo from a path to StormLib DLL.

        :param path_to_stormlib_dll: path to the DLL on the local machine. If not
            provided, will attempt to use an embedded DLL in RichChk.
        :return:
        """
        return StarCraftMpqIo(
            stormlib_wrapper=StormLibHelper.load_stormlib(path_to_stormlib_dll)
        )

    @staticmethod
    def create_wav_io(
        path_to_stormlib_dll: Optional[str] = None,
    ) -> StarCraftWavIo:
        """Create a StarcraftWavIo from a path to StormLib DLL.

        :param path_to_stormlib_dll: path to the DLL on the local machine. If not
            provided, will attempt to use an embedded DLL in RichChk.
        :return:
        """
        return StarCraftWavIo(
            stormlib_wrapper=StormLibHelper.load_stormlib(path_to_stormlib_dll)
        )

    @staticmethod
    def create_wav_metadata_io(
        path_to_stormlib_dll: Optional[str] = None,
    ) -> StarCraftWavMetadataIo:
        """Create a StarcraftWavMetadataIo from a path to StormLib DLL.

        :param path_to_stormlib_dll: path to the DLL on the local machine. If not
            provided, will attempt to use an embedded DLL in RichChk.
        :return:
        """
        return StarCraftWavMetadataIo(
            stormlib_wrapper=StormLibHelper.load_stormlib(path_to_stormlib_dll)
        )
