"""Lookup a Location by its integer index.

This class's main purpose is to resolve location IDs to actual location data when
decoding into a Rich representation. The class can also be used to turn location
references into location IDs when encoding back to the binary CHK.
"""
import dataclasses
import logging
from typing import Optional

from ....util import logger
from .rich_location import RichLocation

_UNUSED_LOCATION_ID = 0


@dataclasses.dataclass(frozen=True)
class RichMrgnLookup:
    _location_by_id_lookup: dict[int, RichLocation]
    _log: logging.Logger = dataclasses.field(
        default_factory=lambda: logger.get_logger(RichMrgnLookup.__name__)
    )

    def get_location_by_id(self, location_id: int) -> Optional[RichLocation]:
        if (
            location_id not in self._location_by_id_lookup
            and location_id != _UNUSED_LOCATION_ID
        ):
            msg = (
                f"No location found for location ID {location_id}."
                + "Verify the location ID is valid."
            )
            self._log.warning(msg)
            raise KeyError(msg)
        elif location_id == _UNUSED_LOCATION_ID:
            self._log.info(
                f"Location ID is {_UNUSED_LOCATION_ID}, meaning the location data is not used."
                f"Returning None value for this location ID."
            )
        return self._location_by_id_lookup.get(location_id)
