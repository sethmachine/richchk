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

from ...model.chk.str.decoded_str_section import DecodedStrSection
from ...transcoder.chk_section_transcoder import ChkSectionTranscoder
from ...transcoder.chk_section_transcoder_factory import _RegistrableTranscoder
from ...transcoder.strings_common import (
    _NULL_TERMINATE_CHAR_FOR_STRING,
    _STRING_ENCODING,
)


class ChkStrTranscoder(
    ChkSectionTranscoder[DecodedStrSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedStrSection.section_name(),
):
    def decode(self, chk_section_binary_data: bytes) -> DecodedStrSection:
        bytes_stream: BytesIO = BytesIO(chk_section_binary_data)
        num_strings: int = struct.unpack("H", bytes_stream.read(2))[0]
        string_offsets: list[int] = []
        for _ in range(num_strings):
            string_offsets.append(struct.unpack("H", bytes_stream.read(2))[0])
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
        return DecodedStrSection(
            _number_of_strings=num_strings,
            _string_offsets=string_offsets,
            _strings=strings,
        )

    def _encode(self, decoded_chk_section: DecodedStrSection) -> bytes:
        data: bytes = b""
        data += struct.pack("H", decoded_chk_section.number_of_strings)
        for i in range(decoded_chk_section.number_of_strings):
            data += struct.pack("H", decoded_chk_section.strings_offsets[i])
        for string_ in decoded_chk_section.strings:
            data += struct.pack(
                "{}s".format(len(string_)), bytes(string_, _STRING_ENCODING)
            )
            data += struct.pack(
                "1s", bytes(_NULL_TERMINATE_CHAR_FOR_STRING, _STRING_ENCODING)
            )
        return data
