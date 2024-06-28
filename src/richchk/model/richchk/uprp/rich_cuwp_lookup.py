"""Lookup CUWP data by its index."""
import dataclasses
import logging
from typing import Optional

from ....util import logger
from .rich_cuwp_slot import RichCuwpSlot


@dataclasses.dataclass(frozen=True)
class RichCuwpLookup:
    _cuwp_by_id_lookup: dict[int, RichCuwpSlot]
    _id_by_cuwp_lookup: dict[RichCuwpSlot, int]
    _log: logging.Logger = dataclasses.field(
        default_factory=lambda: logger.get_logger(RichCuwpLookup.__name__)
    )

    def get_cuwp_by_id(self, id: int) -> Optional[RichCuwpSlot]:
        if id not in self._cuwp_by_id_lookup:
            msg = f"No CUWP found for ID {id}.  IDs should be in range [1, 64]."
            self._log.warning(msg)
            return None
        return self._cuwp_by_id_lookup.get(id)

    def get_id_by_cuwp(self, cuwp: RichCuwpSlot) -> int:
        return self._id_by_cuwp_lookup[cuwp]

    def get_ids(self) -> set[int]:
        return {cuwp_id for cuwp_id in self._cuwp_by_id_lookup.keys()}
