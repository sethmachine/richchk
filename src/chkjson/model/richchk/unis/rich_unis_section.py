import copy
import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection
from .unit_setting import UnitSetting


@dataclasses.dataclass(frozen=True)
class RichUnisSection(RichChkSection):

    _unit_settings: list[UnitSetting]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.UNIS

    @property
    def unit_settings(self) -> list[UnitSetting]:
        return copy.deepcopy(self._unit_settings)
