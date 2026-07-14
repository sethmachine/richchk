"""UPGS - Classic Upgrade Settings (global cost overrides).

Stores global cost override settings for the 46 classic upgrades.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection
from .upgrade_cost_setting import UpgradeCostSetting

_NUM_UPGRADES = 46


@dataclasses.dataclass(frozen=True)
class RichUpgsSection(RichChkSection):
    """Represent UPGS - Classic Upgrade Settings.

    :param _upgrade_cost_settings: list of UpgradeCostSetting, one per upgrade (46
        total)
    """

    _upgrade_cost_settings: list[UpgradeCostSetting]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.UPGS

    @property
    def upgrade_cost_settings(self) -> list[UpgradeCostSetting]:
        return self._upgrade_cost_settings
