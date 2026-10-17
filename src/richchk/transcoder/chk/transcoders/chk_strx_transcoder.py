"""Decode and encode the STRx section which contains all strings in the CHK file."""

import struct
from io import BytesIO
from typing import Optional

from ....model.chk.strx.decoded_strx_section import DecodedStrxSection
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder
from ....transcoder.chk.strings_common import (
    _FALLBACK_MAP_STRING_ENCODING,
    decode_string,
    encode_string,
    resolve_string_encoding,
)
from ....util import logger


class ChkStrxTranscoder(
    ChkSectionTranscoder[DecodedStrxSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedStrxSection.section_name(),
):
    def __init__(self) -> None:
        self._log = logger.get_logger(ChkStrxTranscoder.__name__)

    def decode(
        self,
        chk_section_binary_data: bytes,
        string_encoding: Optional[str] = None,
    ) -> DecodedStrxSection:
        """Decode the STRx section.

        :param string_encoding: the encoding of the strings. If None (or "auto"), it is
            UTF-8 if every string is valid UTF-8, otherwise Windows-1252.
        """
        bytes_stream: BytesIO = BytesIO(chk_section_binary_data)
        num_strings: int = struct.unpack("I", bytes_stream.read(4))[0]
        # Read all offsets at once
        string_offsets = list(
            struct.unpack(f"{num_strings}I", bytes_stream.read(num_strings * 4))
        )
        raw_strings: list[bytes] = []
        # Read bytes until null byte, then decode the full byte sequence
        current_string = bytearray()
        while bytes_stream.tell() != len(chk_section_binary_data):
            char = bytes_stream.read(1)
            if char == b"\0":  # Null terminator
                raw_strings.append(bytes(current_string))
                current_string = bytearray()
            else:
                current_string.extend(char)

        encoding = resolve_string_encoding(string_encoding, raw_strings)
        if encoding == _FALLBACK_MAP_STRING_ENCODING and string_encoding in (
            None,
            "auto",
        ):
            self._log.warning(
                f"The STRx section strings are not valid UTF-8, so they are assumed to "
                f"be {encoding}.  If this is wrong (e.g. a Korean map), read the map "
                f"with an explicit string encoding."
            )
        return DecodedStrxSection(
            _number_of_strings=num_strings,
            _string_offsets=string_offsets,
            _strings=[decode_string(s, encoding) for s in raw_strings],
            _encoding=encoding,
        )

    def _encode(self, decoded_chk_section: DecodedStrxSection) -> bytes:
        # Pre-calculate total size needed
        header_size = 4  # num_strings (2 bytes)
        offsets_size = decoded_chk_section.number_of_strings * 4  # 2 bytes per offset
        strings_size = sum(
            len(encode_string(s, decoded_chk_section.encoding)) + 1
            for s in decoded_chk_section.strings
        )  # +1 for null terminator
        total_size = header_size + offsets_size + strings_size

        data = bytearray(total_size)
        offset = 0

        # Write number of strings
        struct.pack_into("I", data, offset, decoded_chk_section.number_of_strings)
        offset += 4

        # Write all offsets
        struct.pack_into(
            f"{decoded_chk_section.number_of_strings}I",
            data,
            offset,
            *decoded_chk_section.strings_offsets,
        )
        offset += offsets_size

        # Write all strings with null terminators
        for string_ in decoded_chk_section.strings:
            encoded = encode_string(string_, decoded_chk_section.encoding)
            data[offset : offset + len(encoded)] = encoded
            offset += len(encoded)
            data[offset] = 0  # null terminator
            offset += 1

        return bytes(data)
