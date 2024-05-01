"""Contains all the global CHK context needed to produce DecodedChk from RichChk
representations."""

import dataclasses

from ...model.richchk.mrgn.rich_mrgn_lookup import RichMrgnLookup
from ...model.richchk.str.rich_str_lookup import RichStrLookup


@dataclasses.dataclass(frozen=True)
class RichChkEncodeContext:
    _rich_str_lookup: RichStrLookup
    _rich_mrgn_lookup: RichMrgnLookup

    @property
    def rich_str_lookup(self) -> RichStrLookup:
        return self._rich_str_lookup

    @property
    def rich_mrgn_lookup(self) -> RichMrgnLookup:
        return self._rich_mrgn_lookup
