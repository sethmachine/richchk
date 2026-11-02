"""Define the possible CHK section string names that can be found.

The CHK is split into several named chunks (hence the file extension, an abbreviation of
CHunK).

Each section begins with an 8-byte header:

u32 Name - A 4-byte string uniquely identifying that chunk's purpose.
"""

from enum import Enum
from typing import Optional


class ChkSectionName(Enum):
    TYPE = ("TYP ",)
    VER = ("VER ",)
    IVER = ("IVER",)
    IVE2 = ("IVE2",)
    VCOD = ("VCOD",)
    IOWN = ("IOWN",)
    OWNR = ("OWNR",)
    SIDE = ("SIDE",)
    FORC = ("FORC",)
    PUNI = ("PUNI",)
    UPGR = ("UPGR",)
    PTEC = ("PTEC",)
    UPGS = ("UPGS",)
    TECS = ("TECS",)
    PUPX = ("PUPx",)
    PTEX = ("PTEx",)
    UPGX = ("UPGx",)
    TECX = ("TECx",)
    STR = ("STR ",)
    STRX = ("STRx",)
    UNIS = ("UNIS",)
    UNIX = ("UNIx",)
    MRGN = ("MRGN",)
    TRIG = ("TRIG",)
    MBRF = ("MBRF",)
    SPRP = ("SPRP",)
    UPRP = ("UPRP",)
    UPUS = ("UPUS",)
    SWNM = ("SWNM",)
    WAV = ("WAV ",)
    ERA = ("ERA ",)
    DIM = ("DIM ",)
    MTXM = ("MTXM",)
    TILE = ("TILE",)
    ISOM = ("ISOM",)
    DD2 = ("DD2 ",)
    THG2 = ("THG2",)
    MASK = ("MASK",)
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

    @classmethod
    def get_by_bytes(cls, value: bytes) -> Optional["ChkSectionName"]:
        """Find the section named by the 4 raw name bytes of a chunk, if there is
        one."""
        return _SECTION_NAME_BY_BYTES.get(value)


_SECTION_NAME_BY_BYTES: dict[bytes, ChkSectionName] = {
    section_name.value.encode("ascii"): section_name
    for section_name in ChkSectionName
    if section_name != ChkSectionName.UNKNOWN
}
