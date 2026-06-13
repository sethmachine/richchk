"""Tileset for a StarCraft scenario.

See:
https://web.archive.org/web/20250119022852/http://staredit.net//wiki/index.php/Scenario.chk#.22ERA_.22_-_Tileset
"""

from ....model.richchk.richchk_enum import RichChkEnum


class Tileset(RichChkEnum):
    BADLANDS = (0, "Badlands")
    SPACE_PLATFORM = (1, "Space Platform")
    INSTALLATION = (2, "Installation")
    ASHWORLD = (3, "Ashworld")
    JUNGLE = (4, "Jungle")
    DESERT = (5, "Desert")
    ICE = (6, "Ice")
    TWILIGHT = (7, "Twilight")
