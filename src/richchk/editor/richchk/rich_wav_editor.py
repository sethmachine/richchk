"""Add entries for new WAV files.

Do not use this class directly, it should only be used by StarcraftWavIo class.
"""

import logging

from ...model.chk.wav.wav_constants import MAX_WAV_FILES
from ...model.richchk.str.rich_string import RichString
from ...model.richchk.wav.rich_wav import RichWav
from ...model.richchk.wav.rich_wav_section import RichWavSection
from ...util import logger


class RichWavEditor:
    def __init__(self) -> None:
        self.log: logging.Logger = logger.get_logger(RichWavEditor.__name__)

    def add_wav_files(
        self, new_wav_files: list[str], wav: RichWavSection
    ) -> RichWavSection:
        """Add the WAV files to WAV.

        Each new wav file refers to a wav file already added in the MPQ.
        """
        unique_wav_files = self._build_unique_ordered_wavs(new_wav_files)
        allocable_ids = self._generate_allocable_ids(wav)
        wavs_to_add = [x for x in wav.wavs]
        wavs_already_in_wav_section = {x.path_in_chk.value for x in wav.wavs}
        for i, wav_file in enumerate(unique_wav_files):
            if not allocable_ids:
                msg = (
                    f"No more allocable IDs left.  Have we run out of WAV files?  "
                    f"{i + 1} remaining WAV files that cannot be allocated."
                )
                self.log.error(msg)
                raise ValueError(msg)
            if wav_file in wavs_already_in_wav_section:
                self.log.warning(
                    f"Skipping adding a WAV file because its already in the WAV section: {wav_file}"
                )
            else:
                wavs_to_add.append(
                    RichWav(
                        _path_in_chk=RichString(_value=wav_file),
                        _index=allocable_ids.pop(),
                    )
                )
        return RichWavSection(_wavs=wavs_to_add)

    def _build_unique_ordered_wavs(self, wav_files: list[str]) -> list[str]:
        unique_wavs = set(wav_files)
        if len(unique_wavs) < len(wav_files):
            num_duplicates = len(wav_files) - len(unique_wavs)
            self.log.warning(
                f"There are {num_duplicates} duplicate WAV files.  "
                f"Only one of each unique WAV file is allocated to the WAV."
            )
        # TODO: fix this, as tests can cause this to fail since order is not deterministic!
        return wav_files

    @classmethod
    def _generate_allocable_ids(cls, wav: RichWavSection) -> list[int]:
        """Generate all available ids when adding a new wav file to the WAV."""
        possible_ids = range(0, MAX_WAV_FILES)
        already_used_ids = {x.index for x in wav.wavs}
        allocable_ids = [
            index for index in possible_ids if index not in already_used_ids
        ]
        # pop from smallest index to largest
        allocable_ids.reverse()
        return allocable_ids
