"""Edit a RichMrgn section, allocating new location indices where appropriate."""

import logging
from collections.abc import Collection

from ...io.richchk.lookups.mrgn.rich_mrgn_lookup_builder import RichMrgnLookupBuilder
from ...model.chk.mrgn.mrgn_constants import ANYWHERE_LOCATION_ID, MAX_LOCATIONS
from ...model.richchk.mrgn.rich_location import RichLocation
from ...model.richchk.mrgn.rich_mrgn_lookup import RichMrgnLookup
from ...model.richchk.mrgn.rich_mrgn_section import RichMrgnSection
from ...util import logger
from ...util.dataclasses_util import build_dataclass_with_fields


class RichMrgnEditor:
    def __init__(self) -> None:
        self.log: logging.Logger = logger.get_logger(RichMrgnEditor.__name__)

    def add_locations(
        self, locations: Collection[RichLocation], mrgn: RichMrgnSection
    ) -> tuple[RichMrgnSection, RichMrgnLookup]:
        """Add the locations to the MRGN, allocating location indices where
        appropriate."""
        unique_locations_to_add = self._build_location_set(locations)
        location_lookup = RichMrgnLookupBuilder().build_lookup(rich_mrgn=mrgn)
        allocable_indices = self._generate_allocable_location_indices(location_lookup)
        new_locations = [loc for loc in mrgn.locations]
        # TODO: unit test the creation MRGN lookup here too https://github.com/sethmachine/richchk/issues/80
        loc_by_id = {loc.index: loc for loc in new_locations if loc.index is not None}
        id_by_loc = {loc: loc.index for loc in new_locations if loc.index is not None}
        for i, loc in enumerate(unique_locations_to_add):
            if not allocable_indices:
                self.log.error(
                    f"No more allocable indices left.  Have we run out of locations?  "
                    f"{i + 1} remaining locations we cannot allocate."
                )
                break
            if loc.index is not None:
                if not location_lookup.get_location_by_id(loc.index):
                    new_loc = self._build_new_location_with_index(loc, loc.index)
                    new_locations.append(new_loc)
                    assert loc.index is not None
                    loc_by_id[loc.index] = new_loc
                    id_by_loc[new_loc] = loc.index
                    if loc.index in allocable_indices:
                        allocable_indices.remove(loc.index)
                else:
                    self.log.warning(
                        f"Attempted to add a location to the MRGN whose index {loc.index} "
                        f"is already allocated.  "
                        f"Not replacing.  "
                        f"Current location: {location_lookup.get_location_by_id(loc.index)}, "
                        f"Attempted replacement: {loc}"
                    )
            else:
                new_loc = self._build_new_location_with_index(
                    loc, allocable_indices.pop()
                )
                new_locations.append(new_loc)
                assert new_loc.index is not None
                loc_by_id[new_loc.index] = new_loc
                id_by_loc[new_loc] = new_loc.index
                # also store the old loc with a None index
                id_by_loc[loc] = new_loc.index
        new_mrgn = RichMrgnSection(_locations=new_locations)
        return new_mrgn, RichMrgnLookup(
            _location_by_id_lookup=loc_by_id, _id_by_location_lookup=id_by_loc
        )

    def _build_location_set(
        self, locations: Collection[RichLocation]
    ) -> set[RichLocation]:
        """Make all newly added locations unique, so they are not repeated in the MRGN.

        :return:
        """
        unique_locations = set(locations)
        if len(unique_locations) < len(locations):
            num_duplicates = len(locations) - len(unique_locations)
            self.log.warning(
                f"There are {num_duplicates} duplicate locations.  "
                f"Only one of each unique location is allocated to the MRGN."
            )
        # TODO: fix this, as tests can cause this to fail since order is not deterministic!
        return set(locations)

    @classmethod
    def _generate_allocable_location_indices(
        cls, mrgn_lookup: RichMrgnLookup
    ) -> list[int]:
        """Generate all available indices when adding a new location to the MRGN."""
        possible_indices = range(1, MAX_LOCATIONS + 1)
        already_allocated_ids = mrgn_lookup.get_location_ids()
        allocable_indices = [
            index
            for index in possible_indices
            if index not in already_allocated_ids and index != ANYWHERE_LOCATION_ID
        ]
        # pop from smallest index to largest
        allocable_indices.reverse()
        return allocable_indices

    @classmethod
    def _build_new_location_with_index(
        cls, location: RichLocation, index: int
    ) -> RichLocation:
        return build_dataclass_with_fields(location, _index=index)
