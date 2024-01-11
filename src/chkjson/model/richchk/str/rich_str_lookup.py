"""Lookup an STR string by its integer string ID.

Construct this class from a DecodedStrSection using RichStrLookupBuilder.  This class's
main purpose is to decode DecodedChk sections into human-readable RichChk section
representations.
"""
import dataclasses
import logging

from ....model.chk.unis.decoded_unis_section import _STRING_ID_FOR_DEFAULT_UNIT_NAME
from ....util import logger
from .rich_string import RichNullString, RichString


@dataclasses.dataclass(frozen=True)
class RichStrLookup:
    _string_by_id_lookup: dict[int, RichString]
    _log: logging.Logger = dataclasses.field(
        default_factory=lambda: logger.get_logger(RichStrLookup.__name__)
    )

    def get_string_by_id(self, string_id: int) -> RichString:
        if (
            string_id not in self._string_by_id_lookup
            and string_id != _STRING_ID_FOR_DEFAULT_UNIT_NAME
        ):
            self._log.warning(
                f"No string found for string ID {string_id}.  "
                f"Verify the string ID is valid.  "
                f"This will return a RichNullString for non-existent entries."
            )
        elif string_id == _STRING_ID_FOR_DEFAULT_UNIT_NAME:
            self._log.info(
                f"String ID is {_STRING_ID_FOR_DEFAULT_UNIT_NAME}, "
                f"returning RichNullString "
                f"as this means the object uses its default name."
            )
        return self._string_by_id_lookup.get(string_id, RichNullString())
