"""

"""

import abc
import dataclasses
import io
import struct
import typing

from chkjson import logger


def do_twice(func):
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper_do_twice


@dataclasses.dataclass(repr=False)
class _ChkSection(abc.ABC):
    data: typing.Union[io.BytesIO, None] = None

    def __post_init__(self):
        self.log = logger.get_log(self.__class__.__name__)


class ChkSection(abc.ABC):
    # the unique identifying 4 character name of the section, e.g. "TRG "
    name = 'chk section'

    def __init__(self):
        pass

    def __repr__(self):
        return 'CHK Section {}'.format(self.__class__.name)

    @classmethod
    @abc.abstractmethod
    def _decompile(cls, data: io.BytesIO):
        """Decompiles the CHK from a byte stream for this section into a ChkSection object with human readable fields

        :param data:
        :return:
        """
        pass

    @classmethod
    def decompile(cls, data: bytes):
        """Decompiles the CHK bytes for this section into a Chksection object with human readable fields.

        :param data:
        :return:
        """
        return cls._decompile(io.BytesIO(data))

    def _compile_header(self, name, size) -> bytes:
        """Compiles a given string name and size into a CHK section header.

        :return:
        """

        header = struct.pack('{}s'.format(len(name)), bytes(name, 'utf-8'))
        header += struct.pack('I', size)
        return header

    @classmethod
    @abc.abstractmethod
    def compile(self, header=True) -> bytes:
        """Compiles the ChkSection object into the binary format as decompiled from.

        :param header: include the name (u32) and size (u32) headers
        :return:
        """
        pass


if __name__ == '__main__':
    pass
