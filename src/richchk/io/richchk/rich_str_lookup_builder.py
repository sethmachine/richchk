"""Builds a RichChkStrLookup from a DecodedStrSection.

The lookup is used to resolve string IDs to actual string values for human readability
in the RichChk representation.
"""

import logging
from typing import Any, cast

from ...model.chk.decoded_string_section import DecodedStringSection
from ...model.chk.str.decoded_str_section import DecodedStrSection
from ...model.chk.strx.decoded_strx_section import DecodedStrxSection
from ...model.richchk.str.rich_str_lookup import RichStrLookup
from ...model.richchk.str.rich_string import RichString
from ...transcoder.chk.strings_common import _STRING_ENCODING
from ...transcoder.chk.transcoders.chk_str_transcoder import ChkStrTranscoder
from ...transcoder.chk.transcoders.chk_strx_transcoder import ChkStrxTranscoder
from ...util import logger

_lookup_cache: dict[
    Any, Any
] = {}  # id(section) → (section, RichStrLookup) for identity-verified caching


class RichStrLookupBuilder:
    def __init__(self) -> None:
        self._log: logging.Logger = logger.get_logger(RichStrLookupBuilder.__name__)

    def build_lookup(
        self, decoded_string_section: DecodedStringSection
    ) -> RichStrLookup:
        sect_id = id(decoded_string_section)
        cached = _lookup_cache.get(sect_id)
        if cached is not None and cached[0] is decoded_string_section:
            return cast(RichStrLookup, cached[1])
        str_binary_data = self._get_bytes_for_string_section(decoded_string_section)
        _offset_to_rich_string: dict[Any, Any] = {}
        string_by_id = {}
        id_by_string = {}
        idx = str_binary_data.index
        _RichString = RichString
        _encoding = _STRING_ENCODING
        for id_, offset in enumerate(decoded_string_section.strings_offsets):
            # string IDs are 1-indexed (0 denotes no string used)
            actual_string_id = id_ + 1
            rich_string = _offset_to_rich_string.get(offset)
            if rich_string is None:
                end = idx(0, offset)
                rich_string = _RichString(
                    _value=str_binary_data[offset:end].decode(_encoding)
                )
                _offset_to_rich_string[offset] = rich_string
            string_by_id[actual_string_id] = rich_string
            id_by_string[rich_string.value] = actual_string_id
        result = RichStrLookup(
            _string_by_id_lookup=string_by_id, _id_by_string_lookup=id_by_string
        )
        _lookup_cache[sect_id] = (decoded_string_section, result)
        return result

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
        end = str_binary_data.index(0, offset)
        return RichString(_value=str_binary_data[offset:end].decode(_STRING_ENCODING))
