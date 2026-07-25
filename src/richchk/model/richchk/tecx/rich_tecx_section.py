"""TECx - Brood War Tech Settings (global cost overrides).

Stores global cost override settings for all 44 technologies.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection
from ..techs.tech_id import TechId
from ..tecs.tech_cost_setting import TechCostSetting


@dataclasses.dataclass(frozen=True)
class RichTecxSection(RichChkSection):
    """Represent TECx - Brood War Tech Settings.

    :param _tech_cost_settings: dict[TechId, TechCostSetting], one per tech (44 total)
    """

    _tech_cost_settings: dict[TechId, TechCostSetting]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.TECX

    @property
    def tech_cost_settings(self) -> dict[TechId, TechCostSetting]:
        return self._tech_cost_settings
