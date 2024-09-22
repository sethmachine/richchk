"""Search a RichChk for specific WAV files."""

import os

from richchk.io.richchk.query.chk_query_util import ChkQueryUtil
from richchk.model.richchk.rich_chk import RichChk
from richchk.model.richchk.wav.rich_wav import RichWav
from richchk.model.richchk.wav.rich_wav_section import RichWavSection


class WavQueryUtil:
    @staticmethod
    def find_only_wav_by_basename(wav_basename: str, chk: RichChk) -> RichWav:
        # possible edge case if more than 1 WAV file has the same exact basename
        wav_section = ChkQueryUtil.find_only_rich_section_in_chk(RichWavSection, chk)
        # files in MPQ stored with Windows style paths
        wav_by_basename = {
            os.path.basename(x.path_in_chk.value.replace("\\", os.sep)): x
            for x in wav_section.wavs
        }
        maybe_wav = wav_by_basename.get(wav_basename, None)
        if not maybe_wav:
            raise ValueError(
                f"Failed to find the WAV file by basename: {wav_basename}."
                f"All known WAV files in CHK: {wav_by_basename.values()}"
            )
        return maybe_wav

    @staticmethod
    def find_only_wav_by_exact_match(path_to_wav_in_mpq: str, chk: RichChk) -> RichWav:
        wav_section = ChkQueryUtil.find_only_rich_section_in_chk(RichWavSection, chk)
        wav_by_basename = {x.path_in_chk.value: x for x in wav_section.wavs}
        maybe_wav = wav_by_basename.get(path_to_wav_in_mpq, None)
        if not maybe_wav:
            raise ValueError(
                f"Failed to find the WAV file by exact match: {path_to_wav_in_mpq}."
                f"All known WAV files in CHK: {wav_by_basename.keys()}"
            )
        return maybe_wav
