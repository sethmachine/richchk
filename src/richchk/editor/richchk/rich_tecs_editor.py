"""Editor for the TECS - Classic Tech Settings section."""

from ...model.richchk.tecs.rich_tecs_section import RichTecsSection
from ...model.richchk.tecs.tech_cost_setting import TechCostSetting

_NUM_TECHS = 24


class RichTecsEditor:
    def set_tech_cost_setting(
        self,
        setting: TechCostSetting,
        tecs: RichTecsSection,
    ) -> RichTecsSection:
        """Return a new section with the cost setting for a tech replaced.

        :param setting: the new cost setting; setting.tech_id determines which tech to
            replace (must have id < 24)
        :param tecs: the existing TECS section
        :return: new RichTecsSection with the updated setting
        """
        if setting.tech_id.id >= _NUM_TECHS:
            raise ValueError(f"tech id must be < {_NUM_TECHS}, got {setting.tech_id}")
        updated = list(tecs.tech_cost_settings)
        updated[setting.tech_id.id] = setting
        return RichTecsSection(_tech_cost_settings=updated)
