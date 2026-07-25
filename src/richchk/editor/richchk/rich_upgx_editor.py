"""Editor for the UPGx - Brood War Upgrade Settings section."""

from ...model.richchk.upgrades.upgrade_id import UpgradeId
from ...model.richchk.upgs.upgrade_cost_setting import UpgradeCostSetting
from ...model.richchk.upgx.rich_upgx_section import RichUpgxSection


class RichUpgxEditor:
    def set_upgrade_cost_setting(
        self,
        setting: UpgradeCostSetting,
        upgx: RichUpgxSection,
    ) -> RichUpgxSection:
        """Return a new section with the cost setting for an upgrade replaced.

        :param setting: the new cost setting; setting.upgrade_id determines which
            upgrade to replace
        :param upgx: the existing UPGx section
        :return: new RichUpgxSection with the updated setting
        """
        updated = dict(upgx.upgrade_cost_settings)
        updated[setting.upgrade_id] = setting
        return RichUpgxSection(_upgrade_cost_settings=updated)

    def apply_upgrade_cost_settings(
        self,
        updates: dict[UpgradeId, UpgradeCostSetting],
        upgx: RichUpgxSection,
    ) -> RichUpgxSection:
        """Return a new section with cost settings merged from a partial dict.

        Only the upgrade IDs present in `updates` are changed; all others are left as-
        is.

        :param updates: sparse mapping of upgrade -> cost setting
        :param upgx: the existing UPGx section
        :return: new RichUpgxSection with the merged settings applied
        """
        updated = dict(upgx.upgrade_cost_settings)
        updated.update(updates)
        return RichUpgxSection(_upgrade_cost_settings=updated)
