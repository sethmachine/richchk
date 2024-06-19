"""Contains all the global CHK context needed to produce DecodedChk from RichChk
representations."""

import dataclasses

from ...model.richchk.mrgn.rich_mrgn_lookup import RichMrgnLookup
from ...model.richchk.str.rich_str_lookup import RichStrLookup
from .swnm.rich_swnm_lookup import RichSwnmLookup


@dataclasses.dataclass(frozen=True)
class RichChkEncodeContext:
    _rich_str_lookup: RichStrLookup
    _rich_mrgn_lookup: RichMrgnLookup
    _rich_swnm_lookup: RichSwnmLookup

    @property
    def rich_str_lookup(self) -> RichStrLookup:
        return self._rich_str_lookup

    @property
    def rich_mrgn_lookup(self) -> RichMrgnLookup:
        return self._rich_mrgn_lookup

    @property
    def rich_swnm_lookup(self) -> RichSwnmLookup:
        return self._rich_swnm_lookup
