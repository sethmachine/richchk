"""Decode and encode the STR section which contains all strings in the CHK file.

Required for all versions and all game types. Validation: Must be at least 1 byte.

This section contains all the strings in the map.

u16: Number of strings in the section (Default: 1024)

u16[Number of strings]: 1 integer for each string specifying the offset (the spot where
the string starts in the section from the start of it).

Strings: After the offsets, this is where every string in the map goes, one after
another. Each one is terminated by a null character. This section can contain more or
less than 1024 string offsets and will work in Starcraft. Note that STR sections can be
stacked in a similar fashion as MTXM. The exact mechanisms of this are uncertain.

There can be more offsets than actual strings data.  This means some of the offsets
reference the same exact strings.

There is a way to "explode" the representation and make each offset have exactly 1
string corresponding to it. When decoding such a representation, iterate each offset and
look up the string character by character in the remaining string data.

To encode the exploded representation, iterate the parallel list of offsets and strings.
As a string is added to the binary output, first check if it could be found via the
offset.  If it can be found already, there's no need to add the encoded string.

This transcoder does not explode the strings, so there may be more offsets than actual
non-empty string values.
"""

import struct
from io import BytesIO

from ....model.chk.str.decoded_str_section import DecodedStrSection
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder
from ....transcoder.chk.strings_common import _STRING_ENCODING


class ChkStrTranscoder(
    ChkSectionTranscoder[DecodedStrSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedStrSection.section_name(),
):
    def decode(self, chk_section_binary_data: bytes) -> DecodedStrSection:
        bytes_stream: BytesIO = BytesIO(chk_section_binary_data)
        num_strings: int = struct.unpack("H", bytes_stream.read(2))[0]

        # Read all offsets at once
        string_offsets = list(
            struct.unpack(f"{num_strings}H", bytes_stream.read(num_strings * 2))
        )

        strings: list[str] = []
        # there can be more offsets than actual string data,
        # means some offsets reference the same string!
        current_string = bytearray()
        while bytes_stream.tell() != len(chk_section_binary_data):
            char = bytes_stream.read(1)
            if char == b"\0":  # Null terminator
                strings.append(current_string.decode(_STRING_ENCODING))
                current_string = bytearray()
            else:
                current_string.extend(char)

        return DecodedStrSection(
            _number_of_strings=num_strings,
            _string_offsets=string_offsets,
            _strings=strings,
        )

    def _encode(self, decoded_chk_section: DecodedStrSection) -> bytes:
        # Pre-calculate total size needed
        header_size = 2  # num_strings (2 bytes)
        offsets_size = decoded_chk_section.number_of_strings * 2  # 2 bytes per offset
        strings_size = sum(
            len(s.encode(_STRING_ENCODING)) + 1 for s in decoded_chk_section.strings
        )  # +1 for null terminator
        total_size = header_size + offsets_size + strings_size

        data = bytearray(total_size)
        offset = 0

        # Write number of strings
        struct.pack_into("H", data, offset, decoded_chk_section.number_of_strings)
        offset += 2

        # Write all offsets
        struct.pack_into(
            f"{decoded_chk_section.number_of_strings}H",
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
