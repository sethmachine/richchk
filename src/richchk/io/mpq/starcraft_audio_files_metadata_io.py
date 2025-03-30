"""Extract audio files metadata, including durations from a StarCraft MPQ."""
import os
import wave

from mutagen.oggvorbis import OggVorbis

from ...model.mpq.stormlib.stormlib_archive_mode import StormLibArchiveMode
from ...model.mpq.stormlib.stormlib_operation_result import StormLibOperationResult
from ...model.mpq.stormlib.wav.stormlib_wav import StormLibWav
from ...mpq.stormlib.stormlib_file_searcher import StormLibFileSearcher
from ...mpq.stormlib.stormlib_wrapper import StormLibWrapper
from ...util.fileutils import CrossPlatformSafeTemporaryNamedFile


class StarCraftAudioFilesMetadataIo:
    _WAV_FILE_PATTERN = "*.wav"
    _OGG_FILE_PATTERN = "*.ogg"
    _WAV_EXTENSION = ".wav"
    _OGG_EXTENSION = ".ogg"

    def __init__(self, stormlib_wrapper: StormLibWrapper):
        self._stormlib_wrapper = stormlib_wrapper

    def extract_all_audio_files_metadata(
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
        all_ogg_files = file_searcher.find_all_files_matching_pattern(
            self._OGG_FILE_PATTERN
        )
        metadata = []
        for wav in all_wav_files + all_ogg_files:
            duration_ms = self._calculate_audio_file_duration_ms(
                wav, open_archive_result
            )
            metadata.append(
                StormLibWav(_path_to_wav_in_mpq=wav, _duration_ms=duration_ms)
            )
        self._stormlib_wrapper.close_archive(open_archive_result)
        return metadata

    def _calculate_audio_file_duration_ms(
        self, wav_filepath_in_mpq: str, open_archive_result: StormLibOperationResult
    ) -> int:
        with CrossPlatformSafeTemporaryNamedFile(
            suffix=os.path.splitext(wav_filepath_in_mpq)[1]
        ) as temp_wav_file:
            self._stormlib_wrapper.extract_file(
                open_archive_result,
                wav_filepath_in_mpq,
                temp_wav_file,
                overwrite_existing=True,
            )
            if temp_wav_file.endswith(self._WAV_EXTENSION):
                return self._calculate_wav_file_duration_ms(temp_wav_file)
            elif temp_wav_file.endswith(self._OGG_EXTENSION):
                return self._calculate_ogg_file_duration_ms(temp_wav_file)
            else:
                raise ValueError(f"Unsupported audio file {wav_filepath_in_mpq}")

    @classmethod
    def _calculate_wav_file_duration_ms(cls, path_to_wav_file_on_disk: str) -> int:
        with wave.open(path_to_wav_file_on_disk, "rb") as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            duration = frames / float(rate)
            duration_milliseconds = duration * 1000
        return int(duration_milliseconds)

    @classmethod
    def _calculate_ogg_file_duration_ms(cls, path_to_ogg_file_on_disk: str) -> int:
        audio = OggVorbis(path_to_ogg_file_on_disk)
        duration = audio.info.length
        duration_milliseconds = duration * 1000
        return int(duration_milliseconds)
