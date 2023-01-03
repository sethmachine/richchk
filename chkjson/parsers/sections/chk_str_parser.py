"""

"""

import io
import struct

from chkjson.model.chk.chk_section_names import ChkSectionName
from chkjson.model.chk.str.chk_str import ChkStr
from chkjson.parsers.sections.abstract_chk_section_parser import (
    AbstractChkSectionParser,
)

# By default, the first byte in Strings is a NUL character,
# and all unused offsets in the STR section point to this NUL character.
_NULL_CHAR = "\x00"


class ChkStrParser(AbstractChkSectionParser[ChkStr]):
    @property
    def chk_section_name(self) -> ChkSectionName:
        return ChkSectionName.STR

    def parse(self, data: bytes) -> ChkStr:
        byte_stream = io.BytesIO(data)
        num_strings = struct.unpack("H", byte_stream.read(2))[0]
        string_offsets = []
        for i in range(num_strings):
            string_offsets.append(struct.unpack("H", byte_stream.read(2))[0])
        strings = []
        for i in range(num_strings):
            # until null character, read one char at a time,
            # strings won't store the null terminators
            chars = []
            char = struct.unpack("c", byte_stream.read(1))[0].decode("utf-8")
            while char != _NULL_CHAR:
                chars.append(char)
                char = struct.unpack("c", byte_stream.read(1))[0].decode("utf-8")
            strings.append("".join(chars))
        return ChkStr(self.chk_section_name, data, num_strings, string_offsets, strings)

    def compile(self, chk_section: ChkStr, include_header=True) -> bytes:
        data = b""
        if include_header:
            data = self._compile_header(chk_section)
        data += struct.pack("H", chk_section.num_strings)
        for i in range(chk_section.num_strings):
            data += struct.pack("H", chk_section.string_offsets[i])
        for string_ in chk_section.strings:
            data += struct.pack("{}s".format(len(string_)), bytes(string_, "utf-8"))
            data += struct.pack("1s", bytes(_NULL_CHAR, "utf-8"))
        return data


if __name__ == "__main__":
    pass
