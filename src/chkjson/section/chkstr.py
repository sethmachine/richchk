"""

"""


import dataclasses
import io
import struct
import typing

from .abstract_chksection import _ChkSection, ChkSection

NULL_CHAR = '\x00'


@dataclasses.dataclass(repr=False)
class _Fields:
    """Contains all strings in the CHK file.

    Required for all versions and all game types.
    Validation: Must be at least 1 byte.

    This section contains all the strings in the map.

    u16: Number of strings in the section (Default: 1024)
    u16[Number of strings]: 1 integer for each string specifying the offset
    (the spot where the string starts in the section from the start of it).
    Strings: After the offsets, this is where every string in the map goes, one after another.
    Each one is terminated by a null character.
    This section can contain more or less then 1024 string offsests and will work in Starcraft.
    Note that STR sections can be stacked in a smiliar fashion as MTXM. The exact mechanisms of this are uncertain.

    """
    num_strings: int
    string_offsets: typing.List[int]
    strings: typing.List[str]
    stringset: typing.Set[str] = None
    index2string: typing.Dict[int, str] = None


@dataclasses.dataclass(repr=False)
class _Base(_ChkSection, _Fields):
    pass


class ChkStr(_Base, ChkSection):
    """Contains all strings in the CHK file.

    """
    name = 'STR '

    def __post_init__(self):
        self.stringset = set(self.strings)
        self.index2string = {i: text for i, text in enumerate(self.strings)}

    def add_string(self, string_) -> bool:
        """Adds a new string, modifying the binary data accordingly.

        :param string_:
        :return: True if the new string is added, False otherwise (it already exists)
        """
        if string_ in self.stringset:
            self.log.warning('Cannot add string: the string {} already exists.'.format(string_))
            return False
        else:
            # where the new string will start in the data
            new_offset = self.string_offsets[-1] + len(self.strings) + 1
            return True

    def remove_string(self, string_) -> bool:
        if string_ in self.stringset:
            self.log.warning('Cannot remove string: the string {} does not exist.'.format(string_))
            return False
        else:
            return True

    def get_string(self, index) -> str:
        return self.index2string[index]

    @classmethod
    def _decompile(cls, data: io.BytesIO) -> ChkSection:
        num_strings = struct.unpack('H', data.read(2))[0]
        string_offsets = []
        for i in range(num_strings):
            string_offsets.append(struct.unpack('H', data.read(2))[0])
        strings = []
        for i in range(num_strings):
            # until null character, read one char at a time
            chars = []
            char = struct.unpack('c', data.read(1))[0].decode('utf-8')
            while char != NULL_CHAR:
                chars.append(char)
                char = struct.unpack('c', data.read(1))[0].decode('utf-8')
            strings.append(''.join(chars))
        return cls(num_strings=num_strings, string_offsets=string_offsets, strings=strings,
                   data=data.read())

    def compile(self, header=True) -> bytes:
        """

        :return:
        """
        data = b''
        data += struct.pack('H', self.num_strings)
        for i in range(self.num_strings):
            data += struct.pack('H', self.string_offsets[i])
        for string_ in self.strings:
            data += struct.pack('{}s'.format(len(string_)), bytes(string_, 'utf-8'))
            data += struct.pack('1s', bytes(NULL_CHAR, 'utf-8'))
        if header:
            header_ = self._compile_header(self.__class__.name, len(data))
            data = header_ + data
        return data


if __name__ == '__main__':
    c = ChkStr(None, None, None)
    print(c.decompile(None))
