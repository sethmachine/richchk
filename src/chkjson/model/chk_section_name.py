"""Define the possible CHK section string names that can be found.

The CHK is split into several named chunks (hence the file extension, an abbreviation of
CHunK).

Each section begins with an 8-byte header:

u32 Name - A 4-byte string uniquely identifying that chunk's purpose.
"""

from enum import Enum


class ChkSectionName(Enum):
    TYPE = ("TYP ",)
    VER = ("VER ",)
    IVER = ("IVER",)
    IVE2 = ("IVE2",)
    VCOD = ("VCOD",)
    IOWN = ("IOWN",)
    OWNR = ("OWNR",)
    STR = ("STR ",)
    UNIS = ("UNIS",)
    MRGN = ("MRGN",)
    TRIG = ("TRIG",)
    # special case for unhandled/unknown CHK section
    # this does not correspond to any real CHK section name
    UNKNOWN = ("UNKNOWN",)

    def __init__(self, value: str):
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    @classmethod
    def get_by_value(cls, value: str) -> "ChkSectionName":
        return {e.value: e for e in ChkSectionName}[value]

    @classmethod
    def contains(cls, value: str) -> bool:
        return value in {e.value: e for e in ChkSectionName}
