"""Editor for the SPRP - Scenario Properties section."""

from ...model.richchk.sprp.rich_sprp_section import RichSprpSection
from ...model.richchk.str.rich_string import RichString


class RichSprpEditor:
    @staticmethod
    def set_scenario_name(name: RichString, sprp: RichSprpSection) -> RichSprpSection:
        return RichSprpSection(
            _scenario_name=name,
            _scenario_description=sprp.scenario_description,
        )

    @staticmethod
    def set_scenario_description(
        description: RichString, sprp: RichSprpSection
    ) -> RichSprpSection:
        return RichSprpSection(
            _scenario_name=sprp.scenario_name,
            _scenario_description=description,
        )
