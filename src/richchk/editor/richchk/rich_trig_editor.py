"""Add new triggers to a RichTrig section."""

from collections.abc import Collection

from ...model.richchk.trig.rich_trig_section import RichTrigSection
from ...model.richchk.trig.rich_trigger import RichTrigger


class RichTrigEditor:
    @classmethod
    def add_triggers(
        cls, triggers: Collection[RichTrigger], trig: RichTrigSection
    ) -> RichTrigSection:
        """Adds triggers, producing a new RichTrigSection.

        The underlying triggers in the new section are still a shallow copy.  Avoid any
        mutations or side effects.
        """
        new_triggers = [x for x in trig.triggers]
        for new_trigger in triggers:
            new_triggers.append(new_trigger)
        return RichTrigSection(_triggers=new_triggers)
