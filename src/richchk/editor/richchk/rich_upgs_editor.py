"""Editor for the UPGS - Classic Upgrade Settings section."""

from ...model.richchk.upgs.rich_upgs_section import RichUpgsSection
from ...model.richchk.upgs.upgrade_cost_setting import UpgradeCostSetting


class RichUpgsEditor:
    def set_upgrade_cost_setting(
        self,
        setting: UpgradeCostSetting,
        upgs: RichUpgsSection,
    ) -> RichUpgsSection:
        """Return a new section with the cost setting for an upgrade replaced.

        :param setting: the new cost setting; setting.upgrade_id determines which
            upgrade to replace
        :param upgs: the existing UPGS section
        :return: new RichUpgsSection with the updated setting
        """
        updated = dict(upgs.upgrade_cost_settings)
        updated[setting.upgrade_id] = setting
        return RichUpgsSection(_upgrade_cost_settings=updated)
