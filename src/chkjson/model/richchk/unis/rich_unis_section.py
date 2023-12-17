import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection


@dataclasses.dataclass(frozen=True)
class RichUnisSection(RichChkSection):
    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.UNIS
