"""TECS - Classic Tech Settings (global cost overrides).

Stores global cost override settings for the 24 classic technologies.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection
from ..techs.tech_id import TechId
from .tech_cost_setting import TechCostSetting


@dataclasses.dataclass(frozen=True)
class RichTecsSection(RichChkSection):
    """Represent TECS - Classic Tech Settings.

    :param _tech_cost_settings: dict[TechId, TechCostSetting], one per tech (24 total)
    """

    _tech_cost_settings: dict[TechId, TechCostSetting]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.TECS

    @property
    def tech_cost_settings(self) -> dict[TechId, TechCostSetting]:
        return self._tech_cost_settings
