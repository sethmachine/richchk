"""Edit a RichSwnm section, allocating new switch IDs where appropriate."""

import logging
from collections.abc import Collection

from ...model.chk.swnm.swnm_constants import MAX_SWITCHES
from ...model.richchk.swnm.rich_switch import RichSwitch
from ...model.richchk.swnm.rich_swnm_section import RichSwnmSection
from ...util import logger


class RichSwnmEditor:
    def __init__(self) -> None:
        self.log: logging.Logger = logger.get_logger(RichSwnmEditor.__name__)

    def add_switches(
        self, switches: Collection[RichSwitch], swnm: RichSwnmSection
    ) -> RichSwnmSection:
        """Add the switches to the SWNM, allocating switch IDs where appropriate."""
        unique_switches_to_add = self._build_switches_set(switches)
        allocable_ids = self._generate_allocable_ids(swnm)
        new_switches = [x for x in swnm.switches]
        for i, switch in enumerate(unique_switches_to_add):
            if not allocable_ids:
                msg = (
                    f"No more allocable IDs left.  Have we run out of switches?  "
                    f"{i + 1} remaining switches we cannot allocate."
                )
                self.log.error(msg)
                raise ValueError(msg)
            if switch.index is not None:
                if switch not in new_switches:
                    new_switches[switch.index] = switch
                    if switch.index in allocable_ids:
                        allocable_ids.remove(switch.index)
                else:
                    self.log.warning(
                        f"Attempted to add a switch to the SWNM whose ID {switch.index} "
                        f"is already allocated.  "
                        f"Not replacing.  "
                    )
            else:
                new_switches.append(
                    RichSwitch(
                        _custom_name=switch.custom_name, _index=allocable_ids.pop()
                    )
                )
        return RichSwnmSection(_switches=new_switches)

    def _build_switches_set(self, switches: Collection[RichSwitch]) -> set[RichSwitch]:
        unique_switches = set(switches)
        if len(switches) < len(switches):
            num_duplicates = len(switches) - len(unique_switches)
            self.log.warning(
                f"There are {num_duplicates} duplicate switches.  "
                f"Only one of each unique location is allocated to the SWNM."
            )
        return set(switches)

    @classmethod
    def _generate_allocable_ids(cls, swnm: RichSwnmSection) -> list[int]:
        """Generate all available ids when adding a new switch to the SWNM."""
        possible_ids = range(0, MAX_SWITCHES)
        already_used_ids = [x.index for x in swnm.switches if x.index is not None]
        allocable_ids = [
            index for index in possible_ids if index not in already_used_ids
        ]
        # pop from smallest index to largest
        allocable_ids.reverse()
        return allocable_ids
