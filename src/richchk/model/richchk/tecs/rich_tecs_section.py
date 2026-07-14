"""TECS - Classic Tech Settings (global cost overrides).

Stores global cost override settings for the 24 classic technologies.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection
from .tech_cost_setting import TechCostSetting

_NUM_TECHS = 24


@dataclasses.dataclass(frozen=True)
class RichTecsSection(RichChkSection):
    """Represent TECS - Classic Tech Settings.

    :param _tech_cost_settings: list of TechCostSetting, one per tech (24 total)
    """

    _tech_cost_settings: list[TechCostSetting]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.TECS

    @property
    def tech_cost_settings(self) -> list[TechCostSetting]:
        return self._tech_cost_settings
