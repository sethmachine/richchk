"""Modify an existing DecodedStrSection to support newly added strings.

This will preserve the existing string IDs and offsets to ensure they are not broken for
all other CHK sections.
"""

import copy
import logging

from ...io.richchk.rich_str_lookup_builder import RichStrLookupBuilder
from ...model.chk.str.decoded_str_section import DecodedStrSection
from ...transcoder.chk.transcoders.chk_str_transcoder import ChkStrTranscoder
from ...util import logger


class DecodedStrSectionEditor:
    def __init__(self) -> None:
        self.log: logging.Logger = logger.get_logger(DecodedStrSectionEditor.__name__)

    def add_strings_to_str_section(
        self, strings_to_add: list[str], decoded_str_section: DecodedStrSection
    ) -> DecodedStrSection:
        if not strings_to_add:
            self.log.warning(
                "Empty list of strings to add was passed in.  "
                "Not performing any modifications."
            )
            return copy.deepcopy(decoded_str_section)
        new_str_section: DecodedStrSection = self.add_string_to_str_section(
            strings_to_add[0], decoded_str_section
        )
        for remaining_string_to_add in strings_to_add[1:]:
            new_str_section = self.add_string_to_str_section(
                remaining_string_to_add, new_str_section
            )
        return new_str_section

    def add_string_to_str_section(
        self, string_to_add: str, decoded_str_section: DecodedStrSection
    ) -> DecodedStrSection:
        """Add a new string to the STR section, producing a new STR section.

        This method always produces a new DecodedStrSection; the input section is not
        mutated.  The number of strings, the offsets, and the actual strings will be
        updated.  Previous strings encoded will have their IDs and offsets preserved.

        If the added string already exists, no modification will be performed but a deep
        copy of the input section will still be returned.

        :param string_to_add:
        :param decoded_str_section:
        :return:
        """
        if string_to_add in decoded_str_section.strings:
            self.log.warning(
                f'The string "{string_to_add}" already exists in the STR section.  '
                f"Not performing any modifications."
            )
            return copy.deepcopy(decoded_str_section)
        number_of_strings: int = decoded_str_section.number_of_strings + 1
        # increment the previous offsets by 2 bytes,
        # since we'll be adding exactly 1 more offset
        # each additional offset is u16 / takes 2 bytes of space
        string_offsets: list[int] = [
            offset + 2 for offset in decoded_str_section.strings_offsets
        ]
        strings_: list[str] = decoded_str_section.strings.copy()
        # where the new string will start in the data
        # the start of the last string plus its length plus one for the null terminator
        # this assumes the offsets are sorted in increasing size, but this doesn't have to be true!
        highest_offset, highest_string = self._find_highest_offset_and_string(
            decoded_str_section
        )
        # new_offset = string_offsets[-1] + len(strings_[-1]) + 1
        new_offset = (highest_offset + 2) + len(highest_string) + 1
        string_offsets.append(new_offset)
        strings_.append(string_to_add)

        return DecodedStrSection(
            _number_of_strings=number_of_strings,
            _string_offsets=string_offsets,
            _strings=strings_,
        )

    def _find_highest_offset_and_string(
        self, decoded_str_section: DecodedStrSection
    ) -> tuple[int, str]:
        """Finds the highest offset and its corresponding string to determine where to
        allocate a new string."""
        highest_offset = max(decoded_str_section.strings_offsets)
        str_binary_data = ChkStrTranscoder().encode(
            decoded_str_section, include_header=False
        )
        string_for_highest_offset = RichStrLookupBuilder.get_rich_string_by_offset(
            offset=highest_offset, str_binary_data=str_binary_data
        ).value
        return highest_offset, string_for_highest_offset
