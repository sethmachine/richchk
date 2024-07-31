"""Edit a RichUprp section, allocating new CUWP slots."""

import logging
from collections.abc import Collection

from ...io.richchk.lookups.uprp.rich_cuwp_lookup_builder import RichCuwpLookupBuilder
from ...model.chk.uprp.uprp_constants import MAX_CUWP_SLOTS
from ...model.richchk.uprp.rich_cuwp_lookup import RichCuwpLookup
from ...model.richchk.uprp.rich_cuwp_slot import RichCuwpSlot
from ...model.richchk.uprp.rich_uprp_section import RichUprpSection
from ...util import logger
from ...util.dataclasses_util import build_dataclass_with_fields


class RichUprpEditor:
    def __init__(self) -> None:
        self.log: logging.Logger = logger.get_logger(RichUprpEditor.__name__)

    def add_cuwp_slots(
        self, cuwp_slots: Collection[RichCuwpSlot], uprp: RichUprpSection
    ) -> RichUprpSection:
        """Add new CUWP slots to the UPRP, allocating indices where appropriate."""
        unique_cuwps = self._build_set_for_new_entries(cuwp_slots)
        lookup = RichCuwpLookupBuilder().build_lookup_from_rich_uprp(uprp)
        allocable_ids = self._generate_allocable_ids(lookup)
        new_cuwp_slots = [cuwp for cuwp in uprp.cuwp_slots]
        for i, cuwp_to_add in enumerate(unique_cuwps):
            if not allocable_ids:
                msg = (
                    f"No more allocable IDs left.  Have we run out of CUWP slots?  "
                    f"{i + 1} remaining CUWP slots that cannot be allocated."
                )
                self.log.error(msg)
                raise ValueError(msg)
            if cuwp_to_add.index is not None:
                if not lookup.get_cuwp_by_id(cuwp_to_add.index):
                    new_cuwp_slots.append(
                        self._build_new_cuwp_slot_with_index(
                            cuwp_to_add, cuwp_to_add.index
                        )
                    )
                    if cuwp_to_add.index in allocable_ids:
                        allocable_ids.remove(cuwp_to_add.index)
                else:
                    self.log.warning(
                        f"Attempted to add a CUWP to the UPRP whose id {cuwp_to_add.index} "
                        f"is already allocated.  "
                        f"Not replacing.  "
                        f"Current CUWP: {lookup.get_cuwp_by_id(cuwp_to_add.index)}, "
                        f"Attempted replacement: {cuwp_to_add}"
                    )
            else:
                new_cuwp_slots.append(
                    self._build_new_cuwp_slot_with_index(
                        cuwp_to_add, allocable_ids.pop()
                    )
                )
        return RichUprpSection(_cuwp_slots=new_cuwp_slots)

    def _build_set_for_new_entries(
        self, cuwp_slots: Collection[RichCuwpSlot]
    ) -> set[RichCuwpSlot]:
        unique_cuwps = set(cuwp_slots)
        if len(cuwp_slots) < len(cuwp_slots):
            num_duplicates = len(cuwp_slots) - len(unique_cuwps)
            self.log.warning(
                f"There are {num_duplicates} duplicate CUWP slots.  "
                f"Only one of each unique CUWP slot is allocated to the UPRP."
            )
        # TODO: fix this, as tests can cause this to fail since order is not deterministic!
        return unique_cuwps

    @classmethod
    def _generate_allocable_ids(cls, cuwp_lookup: RichCuwpLookup) -> list[int]:
        """Generate all available IDs when adding a new CUWP to the UPRP."""
        # 1-based referencing, not 0-based
        possible_indices = range(1, MAX_CUWP_SLOTS + 1)
        already_allocated_ids = cuwp_lookup.get_ids()
        allocable_ids = [
            index for index in possible_indices if index not in already_allocated_ids
        ]
        # pop from smallest index to largest
        allocable_ids.reverse()
        return allocable_ids

    @classmethod
    def _build_new_cuwp_slot_with_index(
        cls, cuwp_slot: RichCuwpSlot, index: int
    ) -> RichCuwpSlot:
        return build_dataclass_with_fields(cuwp_slot, _index=index)
