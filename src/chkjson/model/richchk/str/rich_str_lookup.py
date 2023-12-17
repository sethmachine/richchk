"""Lookup an STR string by its string ID or string ID by its string value.

Construct this class from a DecodedStrSection.  This class is primarily used to go
between RichChk and DecodedChk representations to construct the STR section and ensure
all string ID references are valid.
"""
import dataclasses


@dataclasses.dataclass(frozen=True)
class RichStrLookup:
    _id_by_string_lookup: dict[str, int]

    def get_id_by_string(self, string_: str) -> int:
        return self._id_by_string_lookup[string_]
