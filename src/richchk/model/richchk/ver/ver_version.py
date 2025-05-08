"""File format version.

See:
https://web.archive.org/web/20250119022852/http://staredit.net//wiki/index.php/Scenario.chk#.22VER_.22_-_Format_Version
"""

from ....model.richchk.richchk_enum import RichChkEnum


class VerVersion(RichChkEnum):
    STARCRAFT_100 = (59, "Starcraft 1.00 (original retail release)")
    STARCRAFT_104 = (63, "Starcraft 1.04 (hybrid)")
    STARCRAFT_REMASTERED_HYBRID = (64, "Starcraft Remastered (1.21) (hybrid)")
    BROOD_WAR_100 = (205, "Brood War 1.00 (1.04)")
    STARCRAFT_REMASTERED_BROODWAR = (206, "Starcraft Remastered (1.21) (broodwar)")
    WARCRAFT_II_RETAIL = (17, "Warcraft II retail (.PUD)")
    WARCRAFT_II_EXPANSION = (19, "Warcraft II Expansion (.PUD)")
    STARCRAFT_BETA = (47, "Starcraft Beta")
    STARCRAFT_PRERELEASE = (57, "Starcraft Prerelease")
    BROOD_WAR_INTERNAL_61 = (61, "Brood War internal (map version 61)")
    BROOD_WAR_INTERNAL_75 = (
        75,
        "Brood War internal (map version 75) (Broodwar Battle.net Beta)",
    )
    BROOD_WAR_INTERNAL_201 = (201, "Brood War internal (map version 201)")
    BROOD_WAR_INTERNAL_203 = (203, "Brood War internal (map version 203)")
