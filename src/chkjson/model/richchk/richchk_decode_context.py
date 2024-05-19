"""Contains all the global CHK context needed to produce RichChk representations."""

import dataclasses

from ...model.richchk.str.rich_str_lookup import RichStrLookup
from .mrgn.rich_mrgn_lookup import RichMrgnLookup


@dataclasses.dataclass(frozen=True)
class RichChkDecodeContext:
    _rich_str_lookup: RichStrLookup
    _rich_mrgn_lookup: RichMrgnLookup = RichMrgnLookup(
        _location_by_id_lookup={}, _id_by_location_lookup={}
    )

    @property
    def rich_str_lookup(self) -> RichStrLookup:
        return self._rich_str_lookup

    @property
    def rich_mrgn_lookup(self) -> RichMrgnLookup:
        return self._rich_mrgn_lookup
