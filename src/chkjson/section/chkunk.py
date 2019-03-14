"""Handler for unknown section names.

"""

import dataclasses
import io

from .abstract_chksection import _ChkSection, ChkSection


@dataclasses.dataclass(repr=False)
class _Fields:
    """Handler for unknown CHK section

    name: the 4 byte name of the unknown section

    """
    name: str = 'UNK '


@dataclasses.dataclass(repr=False)
class _Base(_ChkSection, _Fields):
    pass


class ChkUnk(_Base, ChkSection):
    """Handler for unknown CHK section.


    """
    name = 'UNK '

    @classmethod
    def _decompile(cls, data: io.BytesIO) -> ChkSection:
        return cls(data=data.read())

    def compile(self, header=True) -> bytes:
        return self.data

    def __repr__(self):
        return 'Unknown Section {}'.format(self.name)


if __name__ == '__main__':
    c = ChkUnk(name='foo ')

