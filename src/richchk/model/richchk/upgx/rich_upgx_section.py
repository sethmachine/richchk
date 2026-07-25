"""UPGx - Brood War Upgrade Settings (global cost overrides).

Stores global cost override settings for all 61 upgrades.
"""

import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection
from ..upgrades.upgrade_id import UpgradeId
from ..upgs.upgrade_cost_setting import UpgradeCostSetting


@dataclasses.dataclass(frozen=True)
class RichUpgxSection(RichChkSection):
    """Represent UPGx - Brood War Upgrade Settings.

    :param _upgrade_cost_settings: dict[UpgradeId, UpgradeCostSetting], one per upgrade
        (61 total)
    """

    _upgrade_cost_settings: dict[UpgradeId, UpgradeCostSetting]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.UPGX

    @property
    def upgrade_cost_settings(self) -> dict[UpgradeId, UpgradeCostSetting]:
        return self._upgrade_cost_settings
