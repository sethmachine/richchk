import dataclasses
import io
import struct
import typing

from .abstract_chksection import ChkSection, _ChkSection

NULL_CHAR = "\x00"


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
    string2index: typing.Dict[str, int] = None


@dataclasses.dataclass(repr=False)
class _Base(_ChkSection, _Fields):
    pass


class ChkStr(_Base, ChkSection):
    """Contains all strings in the CHK file."""

    name = "STR "

    def __post_init__(self):
        for cls in self.__class__.__bases__:
            super(self.__class__, self).__post_init__()
        self.stringset = set(self.strings)
        self.index2string = self.__class__._create_index2string(self.strings)
        self.string2index = self.__class__._create_string2index(self.strings)

    @classmethod
    def _create_index2string(cls, strings):
        return {i: text for i, text in enumerate(strings)}

    @classmethod
    def _create_string2index(cls, strings):
        return {text: i for i, text in enumerate(strings)}

    def get_index(self, string_) -> int:
        return self.string2index[string_]

    def get_string(self, index) -> str:
        return self.index2string[index]

    def exists(self, string_) -> bool:
        return string_ in self.stringset

    def add_string(self, string_) -> bool:
        """Adds a new string, updating the number of strings, string offsets, and related fields.

        :param string_:
        :return: True if the new string is added, False otherwise (it already exists)
        """
        if string_ in self.stringset:
            self.log.warning(
                "Cannot add string: the string {} already exists.".format(string_)
            )
            return False
        else:
            # each string offset needs to be incremented by 2
            # because we will be adding a new offset which is 2 bytes
            for i in range(len(self.string_offsets)):
                self.string_offsets[i] += 2
            # where the new string will start in the data
            # the start of the last string plus its length plus one for the null terminator
            new_offset = self.string_offsets[-1] + len(self.strings[-1]) + 1
            self.num_strings += 1
            self.string_offsets.append(new_offset)
            self.strings.append(string_)
            self.stringset.add(string_)
            self.index2string = self.__class__._create_index2string(self.strings)
            self.string2index = self.__class__._create_string2index(self.strings)
            return True

    def remove_string(self, string_) -> int:
        """Removes a string, updating the num strings, offsets, strings, and related fields.

        Note this is a potentially destructive operation, since every other CHK section that refers to
        string data will need to be updated due to indices and offsets shifting by removing the string.

        This method should be invoked within a wrapper method that handles updating the other CHK section
        string references appropriately, and not called directly.

        Does not check if the removed string was used by other sections!

        :param string_:
        :return: the index of the removed string; -1 if no such string exists
        """
        if string_ not in self.stringset:
            self.log.warning(
                "Cannot remove string: the string {} does not exist.".format(string_)
            )
            return -1
        else:
            index = self.string2index[string_]
            offset = self.string_offsets[index]
            size = len(string_) + 1  # for the null terminator
            self.num_strings -= 1
            self.strings.remove(string_)
            self.stringset = set(self.strings)
            self.index2string = self.__class__._create_index2string(self.strings)
            self.string2index = self.__class__._create_string2index(self.strings)
            # update offsets
            self.string_offsets.remove(offset)
            # remove 2 bytes from every offset because we lost 2 bytes from the removed string's offset
            for i in range(len(self.string_offsets)):
                if i < index:
                    self.string_offsets[i] -= 2
                else:
                    self.string_offsets[i] = self.string_offsets[i] - size - 2
            return index

    def get_string(self, index) -> str:
        return self.index2string[index]

    @classmethod
    def _decompile(cls, data: io.BytesIO) -> ChkSection:
        num_strings = struct.unpack("H", data.read(2))[0]
        string_offsets = []
        for i in range(num_strings):
            string_offsets.append(struct.unpack("H", data.read(2))[0])
        strings = []
        for i in range(num_strings):
            # until null character, read one char at a time, strings won't store the null terminators
            chars = []
            char = struct.unpack("c", data.read(1))[0].decode("utf-8")
            while char != NULL_CHAR:
                chars.append(char)
                char = struct.unpack("c", data.read(1))[0].decode("utf-8")
            strings.append("".join(chars))
        return cls(
            num_strings=num_strings,
            string_offsets=string_offsets,
            strings=strings,
            data=data.read(),
        )

    def compile(self, header=True) -> bytes:
        """

        :return:
        """
        data = b""
        data += struct.pack("H", self.num_strings)
        for i in range(self.num_strings):
            data += struct.pack("H", self.string_offsets[i])
        for string_ in self.strings:
            data += struct.pack("{}s".format(len(string_)), bytes(string_, "utf-8"))
            data += struct.pack("1s", bytes(NULL_CHAR, "utf-8"))
        if header:
            header_ = self._compile_header(self.__class__.name, len(data))
            data = header_ + data
        return data

    def to_json(self) -> dict:
        return {
            "num_strings": self.num_strings,
            "string_offsets": self.string_offsets,
            "strings": self.strings,
        }


if __name__ == "__main__":
    c = ChkStr(None, None, None)
    print(c.decompile(None))
