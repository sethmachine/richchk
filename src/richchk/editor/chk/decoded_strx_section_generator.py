"""Generate an STRx from an STR section.

Almost exactly the same, except everything will shift over by 4 bytes total.

2 extra bytes (8 bits) for u32: Number of strings in the section (Default: 1024)

and 2 more extra bytes for each u32[Number of strings]: 1 integer for each string
specifying the offset
"""

import logging

from ...model.chk.str.decoded_str_section import DecodedStrSection
from ...model.chk.strx.decoded_strx_section import DecodedStrxSection
from ...util import logger


class DecodedStrxSectionGenerator:
    def __init__(self) -> None:
        self.log: logging.Logger = logger.get_logger(
            DecodedStrxSectionGenerator.__name__
        )

    def generate_strx_from_str(
        self, decoded_str_section: DecodedStrSection
    ) -> DecodedStrxSection:
        total_byte_shifts = 2 + (len(decoded_str_section.strings_offsets) * 2)
        return DecodedStrxSection(
            _number_of_strings=decoded_str_section.number_of_strings,
            _string_offsets=[
                offset + total_byte_shifts
                for offset in decoded_str_section.strings_offsets
            ],
            _strings=decoded_str_section.strings,
        )
