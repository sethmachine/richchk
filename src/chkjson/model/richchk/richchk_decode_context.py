"""Contains all the global CHK context needed to produce RichChk representations."""

import dataclasses

from ...model.richchk.str.rich_str_lookup import RichStrLookup


@dataclasses.dataclass(frozen=True)
class RichChkDecodeContext:
    _rich_str_lookup: RichStrLookup

    @property
    def rich_str_lookup(self) -> RichStrLookup:
        return self._rich_str_lookup
