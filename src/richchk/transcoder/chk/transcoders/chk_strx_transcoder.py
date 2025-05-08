"""Decode and encode the STRx section which contains all strings in the CHK file."""

import struct
from io import BytesIO

from ....model.chk.strx.decoded_strx_section import DecodedStrxSection
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder
from ....transcoder.chk.strings_common import _STRING_ENCODING


class ChkStrxTranscoder(
    ChkSectionTranscoder[DecodedStrxSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedStrxSection.section_name(),
):
    def decode(self, chk_section_binary_data: bytes) -> DecodedStrxSection:
        bytes_stream: BytesIO = BytesIO(chk_section_binary_data)
        num_strings: int = struct.unpack("I", bytes_stream.read(4))[0]
        # Read all offsets at once
        string_offsets = list(
            struct.unpack(f"{num_strings}I", bytes_stream.read(num_strings * 4))
        )
        strings: list[str] = []
        # Read bytes until null byte, then decode the full byte sequence
        current_string = bytearray()
        while bytes_stream.tell() != len(chk_section_binary_data):
            char = bytes_stream.read(1)
            if char == b"\0":  # Null terminator
                strings.append(current_string.decode(_STRING_ENCODING))
                current_string = bytearray()
            else:
                current_string.extend(char)

        return DecodedStrxSection(
            _number_of_strings=num_strings,
            _string_offsets=string_offsets,
            _strings=strings,
        )

    def _encode(self, decoded_chk_section: DecodedStrxSection) -> bytes:
        # Pre-calculate total size needed
        header_size = 4  # num_strings (2 bytes)
        offsets_size = decoded_chk_section.number_of_strings * 4  # 2 bytes per offset
        strings_size = sum(
            len(s.encode(_STRING_ENCODING)) + 1 for s in decoded_chk_section.strings
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
            encoded = string_.encode(_STRING_ENCODING)
            data[offset : offset + len(encoded)] = encoded
            offset += len(encoded)
            data[offset] = 0  # null terminator
            offset += 1

        return bytes(data)
