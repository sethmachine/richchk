"""Player race types as used in the SIDE section.

See:
http://staredit.net/wiki/index.php/Scenario.chk#.22SIDE.22_-_Player_Races
"""

from ....model.richchk.richchk_enum import RichChkEnum


class PlayerRace(RichChkEnum):
    ZERG = (0x00, "Zerg")
    TERRAN = (0x01, "Terran")
    PROTOSS = (0x02, "Protoss")
    INDEPENDENT = (0x03, "Independent")
    NEUTRAL = (0x04, "Neutral")
    USER_SELECT = (0x05, "User Select")
    RANDOM = (0x06, "Random")
    INACTIVE = (0x07, "Inactive")
