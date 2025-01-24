"""Builds a RichChkStrLookup from a DecodedStrSection.

The lookup is used to resolve string IDs to actual string values for human readability
in the RichChk representation.
"""

import logging
import struct

from ...model.chk.decoded_string_section import DecodedStringSection
from ...model.chk.str.decoded_str_section import DecodedStrSection
from ...model.chk.strx.decoded_strx_section import DecodedStrxSection
from ...model.richchk.str.rich_str_lookup import RichStrLookup
from ...model.richchk.str.rich_string import RichString
from ...transcoder.chk.strings_common import (
    _NULL_TERMINATE_CHAR_FOR_STRING,
    _STRING_ENCODING,
)
from ...transcoder.chk.transcoders.chk_str_transcoder import ChkStrTranscoder
from ...transcoder.chk.transcoders.chk_strx_transcoder import ChkStrxTranscoder
from ...util import logger


class RichStrLookupBuilder:
    def __init__(self) -> None:
        self._log: logging.Logger = logger.get_logger(RichStrLookupBuilder.__name__)

    def build_lookup(
        self, decoded_string_section: DecodedStringSection
    ) -> RichStrLookup:
        str_binary_data = self._get_bytes_for_string_section(decoded_string_section)
        string_by_id = {}
        id_by_string = {}
        for id_, offset in enumerate(decoded_string_section.strings_offsets):
            # string IDs are 1-indexed (0 denotes no string used)
            actual_string_id = id_ + 1
            rich_string = RichStrLookupBuilder.get_rich_string_by_offset(
                offset, str_binary_data
            )
            string_by_id[actual_string_id] = rich_string
            id_by_string[rich_string.value] = actual_string_id
        return RichStrLookup(
            _string_by_id_lookup=string_by_id, _id_by_string_lookup=id_by_string
        )

    def _get_bytes_for_string_section(
        self,
        decoded_string_section: DecodedStringSection,
    ) -> bytes:
        if isinstance(decoded_string_section, DecodedStrSection):
            string_binary_data = ChkStrTranscoder().encode(
                decoded_string_section, include_header=False
            )
        elif isinstance(decoded_string_section, DecodedStrxSection):
            string_binary_data = ChkStrxTranscoder().encode(
                decoded_string_section, include_header=False
            )
        else:
            msg = "Unknown string section.  Expected an STR or STRx but got something else!"
            self._log.error(msg)
            raise ValueError(msg)
        return string_binary_data

    @staticmethod
    def get_rich_string_by_offset(offset: int, str_binary_data: bytes) -> RichString:
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
