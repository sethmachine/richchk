"""Add new briefings to a RichMbrf section."""

from collections.abc import Collection

from ...model.richchk.mbrf.rich_briefing import RichBriefing
from ...model.richchk.mbrf.rich_mbrf_section import RichMbrfSection


class RichMbrfEditor:
    @classmethod
    def add_briefings(
        cls, briefings: Collection[RichBriefing], mbrf: RichMbrfSection
    ) -> RichMbrfSection:
        """Adds briefings, producing a new RichMbrfSection.

        The underlying briefings in the new section are still a shallow copy.  Avoid any
        mutations or side effects.
        """
        return RichMbrfSection(_briefings=list(mbrf.briefings) + list(briefings))
