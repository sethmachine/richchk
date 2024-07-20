""""""
import os
import shutil
import tempfile

from ...io.chk.chk_io import ChkIo
from ...io.richchk.richchk_io import RichChkIo
from ...model.mpq.stormlib.stormlib_archive_mode import StormLibArchiveMode
from ...model.richchk.rich_chk import RichChk
from ...mpq.stormlib.stormlib_wrapper import StormLibWrapper


class StarcraftMpqIo:
    _CHK_MPQ_PATH = "staredit\\scenario.chk"

    def __init__(self, stormlib_wrapper: StormLibWrapper):
        self.stormlib_wrapper = stormlib_wrapper

    def read_chk_from_mpq(self, path_to_starcraft_mpq_file: str) -> RichChk:
        if not os.path.exists(path_to_starcraft_mpq_file):
            raise FileNotFoundError(path_to_starcraft_mpq_file)
        with tempfile.NamedTemporaryFile() as temp_chk_file:
            open_result = self.stormlib_wrapper.open_archive(
                path_to_starcraft_mpq_file, StormLibArchiveMode.STORMLIB_READ_ONLY
            )
            self.stormlib_wrapper.extract_file(
                open_result,
                self._CHK_MPQ_PATH,
                temp_chk_file.name,
                overwrite_existing=True,
            )
            chk = RichChkIo().decode_chk(ChkIo().decode_chk_file(temp_chk_file.name))
            self.stormlib_wrapper.close_archive(open_result)
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
                f"The output MPQ file {path_to_new_mpq_file} already exists."
            )
        with (
            tempfile.NamedTemporaryFile() as temp_chk_file,
            tempfile.NamedTemporaryFile() as temp_mpq_file,
        ):
            ChkIo().encode_chk_to_file(
                RichChkIo().encode_chk(chk), temp_chk_file.name, force_create=True
            )
            shutil.copyfile(path_to_base_mpq_file, temp_mpq_file.name)
            open_result = self.stormlib_wrapper.open_archive(
                temp_mpq_file.name, StormLibArchiveMode.STORMLIB_WRITE_ONLY
            )
            self.stormlib_wrapper.add_file(
                open_result,
                infile=temp_chk_file.name,
                path_to_file_in_archive=self._CHK_MPQ_PATH,
                overwrite_existing=True,
            )
            self.stormlib_wrapper.close_archive(
                self.stormlib_wrapper.compact_archive(open_result)
            )
            shutil.copyfile(temp_mpq_file.name, path_to_new_mpq_file)
