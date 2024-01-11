"""Builds a RichChkStrLookup from a DecodedStrSection.

The lookup is used to resolve string IDs to actual string values for human readability
in the RichChk representation.
"""

import logging
import struct

from ...model.chk.str.decoded_str_section import DecodedStrSection
from ...model.richchk.str.rich_str_lookup import RichStrLookup
from ...model.richchk.str.rich_string import RichString
from ...transcoder.chk.strings_common import (
    _NULL_TERMINATE_CHAR_FOR_STRING,
    _STRING_ENCODING,
)
from ...transcoder.chk.transcoders.chk_str_transcoder import ChkStrTranscoder
from ...util import logger


class RichStrLookupBuilder:
    def __init__(self) -> None:
        self.log: logging.Logger = logger.get_logger(RichStrLookupBuilder.__name__)

    def build_lookup(self, decoded_str_section: DecodedStrSection) -> RichStrLookup:
        transcoder: ChkStrTranscoder = ChkStrTranscoder()
        str_binary_data = transcoder.encode(decoded_str_section, include_header=False)
        string_by_id = {}
        for id_, offset in enumerate(decoded_str_section.strings_offsets):
            # string IDs are 1-indexed (0 denotes no string used)
            string_by_id[id_ + 1] = self._get_rich_string_by_offset(
                offset, str_binary_data
            )
        return RichStrLookup(_string_by_id_lookup=string_by_id)

    def _get_rich_string_by_offset(
        self, offset: int, str_binary_data: bytes
    ) -> RichString:
        current_index = offset
        # read 1 char at a time from the offset until we hit a null terminator
        char: str = struct.unpack("c", bytes([str_binary_data[current_index]]))[
            0
        ].decode(_STRING_ENCODING)
        chars: list[str] = []
        # until null character, read one char at a time,
        # strings won't store the null terminators
        while char != _NULL_TERMINATE_CHAR_FOR_STRING:
            chars.append(char)
            current_index += 1
            char = struct.unpack("c", bytes([str_binary_data[current_index]]))[
                0
            ].decode(_STRING_ENCODING)
        return RichString(_value="".join(chars))
