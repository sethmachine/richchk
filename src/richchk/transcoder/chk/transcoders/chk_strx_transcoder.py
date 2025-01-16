"""Decode and encode the STRx section which contains all strings in the CHK file."""

import struct
from io import BytesIO

from ....model.chk.strx.decoded_strx_section import DecodedStrxSection
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder
from ....transcoder.chk.strings_common import (
    _NULL_TERMINATE_CHAR_FOR_STRING,
    _STRING_ENCODING,
)


class ChkStrxTranscoder(
    ChkSectionTranscoder[DecodedStrxSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedStrxSection.section_name(),
):
    def decode(self, chk_section_binary_data: bytes) -> DecodedStrxSection:
        bytes_stream: BytesIO = BytesIO(chk_section_binary_data)
        num_strings: int = struct.unpack("I", bytes_stream.read(4))[0]
        string_offsets: list[int] = []
        for _ in range(num_strings):
            string_offsets.append(struct.unpack("I", bytes_stream.read(4))[0])
        strings: list[str] = []
        # there can be more offsets than actual string data,
        # means some offsets reference the same string!
        while bytes_stream.tell() != len(chk_section_binary_data):
            char: str = struct.unpack("c", bytes_stream.read(1))[0].decode(
                _STRING_ENCODING
            )
            chars: list[str] = []
            # until null character, read one char at a time,
            # strings won't store the null terminators
            while char != _NULL_TERMINATE_CHAR_FOR_STRING:
                chars.append(char)
                char = struct.unpack("c", bytes_stream.read(1))[0].decode(
                    _STRING_ENCODING
                )
            strings.append("".join(chars))
        return DecodedStrxSection(
            _number_of_strings=num_strings,
            _string_offsets=string_offsets,
            _strings=strings,
        )

    def _encode(self, decoded_chk_section: DecodedStrxSection) -> bytes:
        data: bytes = b""
        data += struct.pack("I", decoded_chk_section.number_of_strings)
        for i in range(decoded_chk_section.number_of_strings):
            data += struct.pack("I", decoded_chk_section.strings_offsets[i])
        for string_ in decoded_chk_section.strings:
            data += struct.pack(
                "{}s".format(len(string_)), bytes(string_, _STRING_ENCODING)
            )
            data += struct.pack(
                "1s", bytes(_NULL_TERMINATE_CHAR_FOR_STRING, _STRING_ENCODING)
            )
        return data
