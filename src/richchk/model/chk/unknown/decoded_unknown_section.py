"""Handler for unknown CHK sections.

UNKNOWN is not an actual CHK section name. This is just convenience to allow handling
partially decoded CHK files.
"""

from dataclasses import dataclass

from ....model.chk.decoded_chk_section import DecodedChkSection
from ....model.chk_section_name import ChkSectionName


@dataclass(frozen=True)
class DecodedUnknownSection(DecodedChkSection):
    """A section kept as raw bytes: its 4 name bytes and its data.

    This holds sections with an unrecognised name and sections that are invalid, so
    neither is interpreted as text and both are written back unchanged.
    """

    _actual_section_name_bytes: bytes
    _chk_binary_data: bytes

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.UNKNOWN

    @classmethod
    def display_name(cls, section_name_bytes: bytes) -> str:
        """Readable form of a section name for logs.

        Never use it to write the name.
        """
        return section_name_bytes.decode("ascii", errors="backslashreplace")

    @property
    def actual_section_name_bytes(self) -> bytes:
        return self._actual_section_name_bytes

    @property
    def actual_section_name(self) -> str:
        return self.display_name(self._actual_section_name_bytes)

    @property
    def chk_binary_data(self) -> bytes:
        return self._chk_binary_data

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(_actual_section_name='{self.actual_section_name}', "
            f"total bytes={len(self._chk_binary_data)})"
        )
