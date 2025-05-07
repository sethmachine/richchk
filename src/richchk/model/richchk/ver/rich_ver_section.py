"""VER - Format Version.

Required for all versions and all game types. Validation: Must be size of 2 bytes.

VER must be 206 in order to use the STRx section.

This section identifies the file format version.

u16: File format version:

59 - Starcraft 1.00 (original retail release)

63 - Starcraft 1.04 (hybrid)

64 - Starcraft Remastered (1.21) (hybrid)

205 - Brood War 1.00 (1.04)

206 - Starcraft Remastered (1.21) (broodwar)

 This is the only version code section to actually be read by StarCraft (of TYPE, VER ,
IVER, and IVE2). Any other value is invalid in retail StarCraft and is usually a beta
version.

Other unsupported versions include:

17 - Warcraft II retail (.PUD)

19 - Warcraft II Expansion (.PUD)

47 - Starcraft Beta

57 - Starcraft Prerelease

61 - Brood War internal (map version 61)

75 - Brood War internal (map version 75) (Broodwar Battle.net Beta)

201 - Brood War internal (map version 201)

203 - Brood War internal (map version 203)
"""
import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection
from .ver_version import VerVersion


@dataclasses.dataclass(frozen=True)
class RichVerSection(RichChkSection):

    _version: VerVersion

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.VER

    @property
    def version(self) -> VerVersion:
        return self._version
