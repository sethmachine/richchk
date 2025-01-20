"""Modify an existing DecodedStrxSection to support newly added strings.

This will preserve the existing string IDs and offsets to ensure they are not broken for
all other CHK sections.
"""

import logging
from collections import OrderedDict

from ...io.richchk.rich_str_lookup_builder import RichStrLookupBuilder
from ...model.chk.strx.decoded_strx_section import DecodedStrxSection
from ...transcoder.chk.transcoders.chk_strx_transcoder import ChkStrxTranscoder
from ...util import logger


class DecodedStrxSectionEditor:
    def __init__(self) -> None:
        self.log: logging.Logger = logger.get_logger(DecodedStrxSectionEditor.__name__)

    def add_strings_to_strx_section(
        self, strings_to_add: list[str], decoded_strx_section: DecodedStrxSection
    ) -> DecodedStrxSection:
        unique_strings_to_add = self._make_strings_to_add_unique(
            strings_to_add, decoded_strx_section
        )
        if not unique_strings_to_add:
            self.log.warning(
                "No new strings to add.  Not performing any modifications."
            )
            return DecodedStrxSection(
                _number_of_strings=decoded_strx_section.number_of_strings,
                _string_offsets=decoded_strx_section.strings_offsets,
                _strings=decoded_strx_section.strings,
            )
        return self._add_strings_to_strx(unique_strings_to_add, decoded_strx_section)

    def _make_strings_to_add_unique(
        self, strings_to_add: list[str], decoded_strx_section: DecodedStrxSection
    ) -> OrderedDict[str, int]:
        """Only add strings not already in the STRx, and which are unique."""
        unique_strings_to_add = OrderedDict()
        already_existing_strings = set(decoded_strx_section.strings)
        for string_to_add in strings_to_add:
            if string_to_add in already_existing_strings:
                self.log.warning(
                    f'The string "{string_to_add}" already exists in the STR section (not adding).'
                )
            else:
                unique_strings_to_add[string_to_add] = 0
        return unique_strings_to_add

    def _add_strings_to_strx(
        self,
        unique_strings_to_add: OrderedDict[str, int],
        decoded_strx_section: DecodedStrxSection,
    ) -> DecodedStrxSection:
        """Add a batch of new strings to the STRx section, producing a new STRx
        section."""

        new_number_of_strings = decoded_strx_section.number_of_strings + len(
            unique_strings_to_add
        )
        # increment the previous offsets by 4 bytes for each new string being added,
        # since we'll be adding exactly 1 more offset
        # each additional offset is u32 / takes 4 bytes of space
        total_offset_increase = len(unique_strings_to_add) * 4
        new_string_offsets = [
            offset + total_offset_increase
            for offset in decoded_strx_section.strings_offsets
        ]
        # where the new string will start in the data
        # the start of the last string plus its length plus one for the null terminator
        # this assumes the offsets are sorted in increasing size, but this doesn't have to be true!
        highest_offset = None
        highest_string = None
        for string_to_add in unique_strings_to_add:
            if highest_offset is None and highest_string is None:
                (
                    highest_offset,
                    highest_string,
                ) = self._find_initial_highest_offset_and_string(decoded_strx_section)
                new_offset = (
                    (highest_offset + total_offset_increase) + len(highest_string) + 1
                )
            else:
                # if they are defined, we use the previous string offset we just added
                # new_offset = string_offsets[-1] + len(strings_[-1]) + 1
                # +1 is there to skip the null terminator
                new_offset = highest_offset + len(highest_string) + 1
            new_string_offsets.append(new_offset)
            # set up the next string being added, if any
            highest_offset = new_offset
            highest_string = string_to_add
        return DecodedStrxSection(
            _number_of_strings=new_number_of_strings,
            _string_offsets=new_string_offsets,
            _strings=decoded_strx_section.strings + list(unique_strings_to_add.keys()),
        )

    def _find_initial_highest_offset_and_string(
        self, decoded_strx_section: DecodedStrxSection
    ) -> tuple[int, str]:
        """Finds the initial highest offset and its corresponding string to determine
        where to allocate a new string."""
        highest_offset = max(decoded_strx_section.strings_offsets)
        str_binary_data = ChkStrxTranscoder().encode(
            decoded_strx_section, include_header=False
        )
        string_for_highest_offset = RichStrLookupBuilder.get_rich_string_by_offset(
            offset=highest_offset, str_binary_data=str_binary_data
        ).value
        return highest_offset, string_for_highest_offset
