"""Editor for the TECS - Classic Tech Settings section."""

from ...model.richchk.techs.tech_id import TechId
from ...model.richchk.tecs.rich_tecs_section import RichTecsSection
from ...model.richchk.tecs.tech_cost_setting import TechCostSetting


class RichTecsEditor:
    def set_tech_cost_setting(
        self,
        setting: TechCostSetting,
        tecs: RichTecsSection,
    ) -> RichTecsSection:
        """Return a new section with the cost setting for a tech replaced.

        :param setting: the new cost setting; setting.tech_id determines which tech to
            replace
        :param tecs: the existing TECS section
        :return: new RichTecsSection with the updated setting
        """
        updated = dict(tecs.tech_cost_settings)
        updated[setting.tech_id] = setting
        return RichTecsSection(_tech_cost_settings=updated)

    def apply_tech_cost_settings(
        self,
        updates: dict[TechId, TechCostSetting],
        tecs: RichTecsSection,
    ) -> RichTecsSection:
        """Return a new section with cost settings merged from a partial dict.

        Only the tech IDs present in `updates` are changed; all others are left as-is.

        :param updates: sparse mapping of tech -> cost setting
        :param tecs: the existing TECS section
        :return: new RichTecsSection with the merged settings applied
        """
        updated = dict(tecs.tech_cost_settings)
        updated.update(updates)
        return RichTecsSection(_tech_cost_settings=updated)
