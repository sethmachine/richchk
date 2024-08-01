"""Lookup metadata about WAV files contained in a StarCraft MPQ.

This is primarily used to expose the WAV file's millisecond duration for automatic
completion in trigger actions.
"""

import dataclasses
from typing import Optional

from ...mpq.stormlib.wav.stormlib_wav import StormLibWav


@dataclasses.dataclass(frozen=True)
class RichWavMetadataLookup:
    _metadata_by_wav_path: dict[str, StormLibWav]

    def get_metadata_by_wav_path(
        self, path_to_wav_in_mpq: str
    ) -> Optional[StormLibWav]:
        return self._metadata_by_wav_path.get(path_to_wav_in_mpq, None)
