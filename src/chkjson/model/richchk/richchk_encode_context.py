"""Contains all the global CHK context needed to produce DecodedChk from RichChk
representations."""

import copy
import dataclasses

from ...model.richchk.str.rich_str_lookup import RichStrLookup


@dataclasses.dataclass(frozen=True)
class RichChkEncodeContext:
    _rich_str_lookup: RichStrLookup

    @property
    def rich_str_lookup(self) -> RichStrLookup:
        return copy.deepcopy(self._rich_str_lookup)
