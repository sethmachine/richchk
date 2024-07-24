"""Extract WAV files metadata, including durations from a StarCraft MPQ."""
import os
import tempfile
import wave

from ...model.mpq.stormlib.stormlib_archive_mode import StormLibArchiveMode
from ...model.mpq.stormlib.stormlib_operation_result import StormLibOperationResult
from ...model.mpq.stormlib.wav.stormlib_wav import StormLibWav
from ...mpq.stormlib.stormlib_file_searcher import StormLibFileSearcher
from ...mpq.stormlib.stormlib_wrapper import StormLibWrapper


class StarcraftWavMetadataIo:
    _WAV_FILE_PATTERN = "*.wav"

    def __init__(self, stormlib_wrapper: StormLibWrapper):
        self._stormlib_wrapper = stormlib_wrapper

    def extract_all_wav_files_metadata(
        self, path_to_starcraft_mpq_file: str
    ) -> list[StormLibWav]:
        """Extract metadata of all WAV files in the MPQ archive, including duration in
        milliseconds.

        :param path_to_starcraft_mpq_file:
        :return:
        """
        if not os.path.exists(path_to_starcraft_mpq_file):
            raise FileNotFoundError(path_to_starcraft_mpq_file)
        open_archive_result = self._stormlib_wrapper.open_archive(
            path_to_starcraft_mpq_file, StormLibArchiveMode.STORMLIB_WRITE_ONLY
        )
        file_searcher = StormLibFileSearcher(
            stormlib_reference=self._stormlib_wrapper.stormlib,
            open_mpq_handle=open_archive_result,
        )
        all_wav_files = file_searcher.find_all_files_matching_pattern(
            self._WAV_FILE_PATTERN
        )
        metadata = []
        for wav in all_wav_files:
            duration_ms = self._calculate_wav_file_duration_in_mpq(
                wav, open_archive_result
            )
            metadata.append(
                StormLibWav(_path_to_wav_in_mpq=wav, _duration_ms=duration_ms)
            )
        self._stormlib_wrapper.close_archive(open_archive_result)
        return metadata

    def add_wav_files_to_mpq(
        self,
        path_to_wavs_on_disk: list[str],
        path_to_base_mpq_file: str,
        path_to_new_mpq_file: str,
        overwrite_existing: bool = False,
    ) -> None:
        """Adds WAV files to the Starcraft MPQ, also updating the WAV and STR sections
        in the CHK.

        :param path_to_wavs_on_disk:
        :param path_to_base_mpq_file:
        :param path_to_new_mpq_file:
        :param overwrite_existing:
        :return:
        """
        if not all((os.path.exists(wav) for wav in path_to_wavs_on_disk)):
            raise FileNotFoundError(
                f"At least one WAV file does not exist: {path_to_wavs_on_disk}"
            )
        if not os.path.exists(path_to_base_mpq_file):
            raise FileNotFoundError(path_to_base_mpq_file)
        if os.path.exists(path_to_new_mpq_file) and not overwrite_existing:
            raise FileExistsError(
                f"The output MPQ file {path_to_new_mpq_file} already exists."
            )
        pass

    def _calculate_wav_file_duration_in_mpq(
        self, wav_filepath_in_mpq: str, open_archive_result: StormLibOperationResult
    ) -> int:
        with tempfile.NamedTemporaryFile() as temp_wav_file:
            self._stormlib_wrapper.extract_file(
                open_archive_result,
                wav_filepath_in_mpq,
                temp_wav_file.name,
                overwrite_existing=True,
            )
            return self._calculate_wav_file_duration_ms(temp_wav_file.name)

    @classmethod
    def _calculate_wav_file_duration_ms(cls, path_to_wav_file_on_disk: str) -> int:
        with wave.open(path_to_wav_file_on_disk, "rb") as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            duration = frames / float(rate)
            duration_milliseconds = duration * 1000
        return int(duration_milliseconds)
