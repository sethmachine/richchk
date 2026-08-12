"""SPRP - Scenario Properties.

Required for all versions and all game types. Validation: Must be size of 4 bytes.

u16: String number of the scenario name u16: String number of the scenario description
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..decoded_chk_section import DecodedChkSection


@dataclasses.dataclass(frozen=True)
class DecodedSprpSection(DecodedChkSection):
    """Represent SPRP - Scenario Properties.

    :param _scenario_name_string_id: u16 string ID for the scenario name
    :param _scenario_description_string_id: u16 string ID for the scenario description
    """

    _scenario_name_string_id: int
    _scenario_description_string_id: int

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.SPRP

    @property
    def scenario_name_string_id(self) -> int:
        return self._scenario_name_string_id

    @property
    def scenario_description_string_id(self) -> int:
        return self._scenario_description_string_id
