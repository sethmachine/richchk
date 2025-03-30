""""""
import os
import shutil

from ...io.chk.chk_io import ChkIo
from ...io.richchk.richchk_io import RichChkIo
from ...model.mpq.stormlib.stormlib_archive_mode import StormLibArchiveMode
from ...model.richchk.rich_chk import RichChk
from ...model.richchk.wav.rich_wav_metadata_lookup import RichWavMetadataLookup
from ...mpq.stormlib.stormlib_wrapper import StormLibWrapper
from ...util.fileutils import CrossPlatformSafeTemporaryNamedFile
from .starcraft_audio_files_metadata_io import StarCraftAudioFilesMetadataIo


class StarCraftMpqIo:
    _CHK_MPQ_PATH = "staredit\\scenario.chk"

    def __init__(self, stormlib_wrapper: StormLibWrapper):
        self._stormlib_wrapper = stormlib_wrapper

    def extract_chk_from_mpq(
        self,
        path_to_starcraft_mpq_file: str,
        outfile: str,
        overwrite_existing: bool = True,
    ) -> None:
        if not os.path.exists(path_to_starcraft_mpq_file):
            raise FileNotFoundError(path_to_starcraft_mpq_file)
        open_result = self._stormlib_wrapper.open_archive(
            path_to_starcraft_mpq_file, StormLibArchiveMode.STORMLIB_READ_ONLY
        )
        self._stormlib_wrapper.extract_file(
            open_result,
            self._CHK_MPQ_PATH,
            outfile,
            overwrite_existing=overwrite_existing,
        )
        self._stormlib_wrapper.close_archive(open_result)

    def read_chk_from_mpq(self, path_to_starcraft_mpq_file: str) -> RichChk:
        if not os.path.exists(path_to_starcraft_mpq_file):
            raise FileNotFoundError(path_to_starcraft_mpq_file)
        with CrossPlatformSafeTemporaryNamedFile() as temp_chk_file:
            open_result = self._stormlib_wrapper.open_archive(
                path_to_starcraft_mpq_file, StormLibArchiveMode.STORMLIB_READ_ONLY
            )
            self._stormlib_wrapper.extract_file(
                open_result,
                self._CHK_MPQ_PATH,
                temp_chk_file,
                overwrite_existing=True,
            )
            chk = RichChkIo().decode_chk(ChkIo().decode_chk_file(temp_chk_file))
            self._stormlib_wrapper.close_archive(open_result)
            return chk

    def save_chk_to_mpq(
        self,
        chk: RichChk,
        path_to_base_mpq_file: str,
        path_to_new_mpq_file: str,
        overwrite_existing: bool = False,
    ) -> None:
        if not os.path.exists(path_to_base_mpq_file):
            raise FileNotFoundError(path_to_base_mpq_file)
        if os.path.exists(path_to_new_mpq_file) and not overwrite_existing:
            raise FileExistsError(
                f"Refusing to create new MPQ because it already exists: {path_to_new_mpq_file}"
            )
        with (
            CrossPlatformSafeTemporaryNamedFile() as temp_chk_file,
            CrossPlatformSafeTemporaryNamedFile() as temp_mpq_file,
        ):

            ChkIo().encode_chk_to_file(
                RichChkIo().encode_chk(
                    rich_chk=chk,
                    wav_metadata_lookup=self._build_wav_metadata_lookup(
                        path_to_base_mpq_file
                    ),
                ),
                temp_chk_file,
                force_create=True,
            )
            shutil.copyfile(path_to_base_mpq_file, temp_mpq_file)
            open_result = self._stormlib_wrapper.open_archive(
                temp_mpq_file, StormLibArchiveMode.STORMLIB_WRITE_ONLY
            )
            self._stormlib_wrapper.add_file(
                open_result,
                infile=temp_chk_file,
                path_to_file_in_archive=self._CHK_MPQ_PATH,
                overwrite_existing=True,
            )
            self._stormlib_wrapper.close_archive(
                self._stormlib_wrapper.compact_archive(open_result)
            )
            shutil.copyfile(temp_mpq_file, path_to_new_mpq_file)

    def _build_wav_metadata_lookup(
        self, path_to_base_mpq_file: str
    ) -> RichWavMetadataLookup:
        wav_metadata = StarCraftAudioFilesMetadataIo(
            stormlib_wrapper=self._stormlib_wrapper
        ).extract_all_audio_files_metadata(path_to_base_mpq_file)
        return RichWavMetadataLookup(
            _metadata_by_wav_path={x.path_to_wav_in_mpq: x for x in wav_metadata}
        )
