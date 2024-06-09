"""Lookup switch string data by its index."""
import dataclasses
import logging
from typing import Optional

from ....util import logger
from .rich_switch import RichSwitch


@dataclasses.dataclass(frozen=True)
class RichSwnmLookup:
    _switch_by_id_lookup: dict[int, RichSwitch]
    _id_by_switch_lookup: dict[RichSwitch, int]
    _log: logging.Logger = dataclasses.field(
        default_factory=lambda: logger.get_logger(RichSwnmLookup.__name__)
    )

    def get_switch_by_id(self, switch_id: int) -> Optional[RichSwitch]:
        if switch_id not in self._switch_by_id_lookup:
            msg = f"No RichSwitch found for switch ID {switch_id}.  Switch IDs should be in range [0, 255]."
            self._log.warning(msg)
            return None
        return self._switch_by_id_lookup.get(switch_id)

    def get_id_by_switch(self, switch: RichSwitch) -> int:
        return self._id_by_switch_lookup[switch]
