"""UNIx - Brood War unit settings.

Exactly the same as the UNIS section except this section supports 130 weapons.
"""
import copy
import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection
from ..unis.unit_setting import UnitSetting


@dataclasses.dataclass(frozen=True)
class RichUnixSection(RichChkSection):

    _unit_settings: list[UnitSetting]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.UNIX

    @property
    def unit_settings(self) -> list[UnitSetting]:
        return copy.deepcopy(self._unit_settings)
