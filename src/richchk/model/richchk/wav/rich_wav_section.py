"""WAV - WAV String Indexes.

Contains only WAV entries that are used or referenced in trigger data.

Do not edit this section directly.  Instead, first add WAV files through Stormlib APIs.
"""
import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection
from .rich_wav import RichWav


@dataclasses.dataclass(frozen=True)
class RichWavSection(RichChkSection):

    _wavs: list[RichWav]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.WAV

    @property
    def wavs(self) -> list[RichWav]:
        return self._wavs
