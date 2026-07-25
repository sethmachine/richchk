"""Editor for the TECx - Brood War Tech Settings section."""

from ...model.richchk.techs.tech_id import TechId
from ...model.richchk.tecs.tech_cost_setting import TechCostSetting
from ...model.richchk.tecx.rich_tecx_section import RichTecxSection


class RichTecxEditor:
    def set_tech_cost_setting(
        self,
        setting: TechCostSetting,
        tecx: RichTecxSection,
    ) -> RichTecxSection:
        """Return a new section with the cost setting for a tech replaced.

        :param setting: the new cost setting; setting.tech_id determines which tech to
            replace
        :param tecx: the existing TECx section
        :return: new RichTecxSection with the updated setting
        """
        updated = dict(tecx.tech_cost_settings)
        updated[setting.tech_id] = setting
        return RichTecxSection(_tech_cost_settings=updated)

    def apply_tech_cost_settings(
        self,
        updates: dict[TechId, TechCostSetting],
        tecx: RichTecxSection,
    ) -> RichTecxSection:
        """Return a new section with cost settings merged from a partial dict.

        Only the tech IDs present in `updates` are changed; all others are left as-is.

        :param updates: sparse mapping of tech -> cost setting
        :param tecx: the existing TECx section
        :return: new RichTecxSection with the merged settings applied
        """
        updated = dict(tecx.tech_cost_settings)
        updated.update(updates)
        return RichTecxSection(_tech_cost_settings=updated)
