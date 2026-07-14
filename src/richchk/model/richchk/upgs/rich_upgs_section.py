"""UPGS - Classic Upgrade Settings (global cost overrides).

Stores global cost override settings for the 46 classic upgrades.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection
from ..upgrades.upgrade_id import UpgradeId
from .upgrade_cost_setting import UpgradeCostSetting


@dataclasses.dataclass(frozen=True)
class RichUpgsSection(RichChkSection):
    """Represent UPGS - Classic Upgrade Settings.

    :param _upgrade_cost_settings: dict[UpgradeId, UpgradeCostSetting], one per upgrade
        (46 total)
    """

    _upgrade_cost_settings: dict[UpgradeId, UpgradeCostSetting]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.UPGS

    @property
    def upgrade_cost_settings(self) -> dict[UpgradeId, UpgradeCostSetting]:
        return self._upgrade_cost_settings
