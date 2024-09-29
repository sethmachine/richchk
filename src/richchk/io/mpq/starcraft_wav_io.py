"""Add WAV files to a StarCraft MPQ and update the WAV/STR sections in the CHK."""
import os
import shutil
import tempfile

from ...editor.richchk.rich_chk_editor import RichChkEditor
from ...editor.richchk.rich_wav_editor import RichWavEditor
from ...model.mpq.stormlib.stormlib_archive_mode import StormLibArchiveMode
from ...model.richchk.rich_chk import RichChk
from ...model.richchk.wav.rich_wav_section import RichWavSection
from ...mpq.stormlib.stormlib_wrapper import StormLibWrapper
from ..richchk.query.chk_query_util import ChkQueryUtil
from .starcraft_mpq_io import StarCraftMpqIo


class StarCraftWavIo:

    # canonical location where WAV files are stored in a StarCraft MPQ
    _WAV_DIRECTORY = "staredit\\wav"

    def __init__(self, stormlib_wrapper: StormLibWrapper):
        self._stormlib_wrapper = stormlib_wrapper
        self._starcraft_mpq_io = StarCraftMpqIo(stormlib_wrapper=stormlib_wrapper)

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
        with (tempfile.NamedTemporaryFile() as temp_mpq_file):
            shutil.copyfile(path_to_base_mpq_file, temp_mpq_file.name)
            new_wav_files = self._add_wavfiles_to_mpq(
                path_to_mpq_file=temp_mpq_file.name,
                path_to_wavs_on_disk=path_to_wavs_on_disk,
            )
            new_chk = self._update_chk_wav_section(temp_mpq_file.name, new_wav_files)
            self._starcraft_mpq_io.save_chk_to_mpq(
                new_chk,
                path_to_base_mpq_file=temp_mpq_file.name,
                path_to_new_mpq_file=path_to_new_mpq_file,
                overwrite_existing=True,
            )

    def _add_wavfiles_to_mpq(
        self,
        path_to_mpq_file: str,
        path_to_wavs_on_disk: list[str],
    ) -> list[str]:
        """Add each WAV file to the open MPQ.  This does not update the CHK WAV or STR
        sections!

        :param path_to_wavs_on_disk: the paths to each added WAV file in the MPQ
        :return:
        """
        open_archive_result = self._stormlib_wrapper.open_archive(
            path_to_mpq_file, StormLibArchiveMode.STORMLIB_WRITE_ONLY
        )
        path_to_wavs_in_mpq = []
        for wavfile in path_to_wavs_on_disk:
            wavfile_in_mpq = self._create_wav_filepath_in_mpq(wavfile)
            path_to_wavs_in_mpq.append(wavfile_in_mpq)
            self._stormlib_wrapper.add_file(
                open_archive_result,
                infile=wavfile,
                path_to_file_in_archive=wavfile_in_mpq,
                overwrite_existing=True,
            )
        self._stormlib_wrapper.compact_archive(open_archive_result)
        self._stormlib_wrapper.close_archive(open_archive_result)
        return path_to_wavs_in_mpq

    @classmethod
    def _create_wav_filepath_in_mpq(cls, path_to_wav_on_disk: str) -> str:
        bn = os.path.basename(path_to_wav_on_disk)
        return cls._WAV_DIRECTORY + "\\" + bn

    def _update_chk_wav_section(
        self, path_to_mpq_file: str, new_wav_files: list[str]
    ) -> RichChk:
        chk = self._starcraft_mpq_io.read_chk_from_mpq(path_to_mpq_file)
        new_wav = self._update_wav_with_new_wav_files(new_wav_files, chk)
        new_chk = RichChkEditor().replace_chk_section(new_wav, chk)
        return new_chk

    def _update_wav_with_new_wav_files(
        self, new_wav_files: list[str], chk: RichChk
    ) -> RichWavSection:
        rich_wav = ChkQueryUtil.find_only_rich_section_in_chk(RichWavSection, chk)
        new_wav = RichWavEditor().add_wav_files(new_wav_files, rich_wav)
        return new_wav
