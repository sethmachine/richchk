"""SPRP - Scenario Properties.

Required for all versions and all game types. Validation: Must be size of 4 bytes.

u16: String number of the scenario name u16: String number of the scenario description
"""
import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection
from ..str.rich_string import RichString


@dataclasses.dataclass(frozen=True)
class RichSprpSection(RichChkSection):

    _scenario_name: RichString
    _scenario_description: RichString

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.SPRP

    @property
    def scenario_name(self) -> RichString:
        return self._scenario_name

    @property
    def scenario_description(self) -> RichString:
        return self._scenario_description
