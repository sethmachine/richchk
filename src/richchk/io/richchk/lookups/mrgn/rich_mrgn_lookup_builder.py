"""Builds a RichMrgnLookup from a DecodedMrgnSection.

The lookup is used to resolve location IDs to actual location data for human readability
in the RichChk representation.
"""

import logging

from .....model.richchk.mrgn.rich_mrgn_lookup import RichMrgnLookup
from .....model.richchk.mrgn.rich_mrgn_section import RichMrgnSection
from .....util import logger


class RichMrgnLookupBuilder:
    def __init__(self) -> None:
        self.log: logging.Logger = logger.get_logger(RichMrgnLookupBuilder.__name__)

    def build_lookup(self, rich_mrgn: RichMrgnSection) -> RichMrgnLookup:
        location_by_id = {}
        id_by_location = {}
        for location in rich_mrgn.locations:
            if location.index is None:
                msg = f"Unable to build MRGN lookup if a location has not been allocated an index: {location}"
                self.log.error(msg)
                raise ValueError(msg)
            # location IDs are 1-indexed (0 denotes no location used/referenced)
            location_by_id[location.index] = location
            id_by_location[location] = location.index
        return RichMrgnLookup(
            _location_by_id_lookup=location_by_id, _id_by_location_lookup=id_by_location
        )
