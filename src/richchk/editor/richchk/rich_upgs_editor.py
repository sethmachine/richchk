"""Editor for the UPGS - Classic Upgrade Settings section."""

from ...model.richchk.upgs.rich_upgs_section import RichUpgsSection
from ...model.richchk.upgs.upgrade_cost_setting import UpgradeCostSetting

_NUM_UPGRADES = 46


class RichUpgsEditor:
    def set_upgrade_cost_setting(
        self,
        setting: UpgradeCostSetting,
        upgs: RichUpgsSection,
    ) -> RichUpgsSection:
        """Return a new section with the cost setting for an upgrade replaced.

        :param setting: the new cost setting; setting.upgrade_id determines which
            upgrade to replace (must have id < 46)
        :param upgs: the existing UPGS section
        :return: new RichUpgsSection with the updated setting
        """
        if setting.upgrade_id.id >= _NUM_UPGRADES:
            raise ValueError(
                f"upgrade id must be < {_NUM_UPGRADES} for UPGS (classic only), "
                f"got {setting.upgrade_id}"
            )
        updated = list(upgs.upgrade_cost_settings)
        updated[setting.upgrade_id.id] = setting
        return RichUpgsSection(_upgrade_cost_settings=updated)
