"""Score type.

See: http://www.staredit.net/wiki/index.php/Scenario.chk#Score_Types
"""

from chkjson.model.richchk.richchk_enum import RichChkEnum


class ScoreType(RichChkEnum):
    TOTAL = (0, "Total")
    UNITS = (1, "Units")
    BUILDINGS = (2, "Buildings")
    UNITS_AND_BUILDINGS = (3, "Units and Buildings")
    KILLS = (4, "Kills")
    RAZINGS = (5, "Razings")
    KILLS_AND_RAZINGS = (6, "Kills and Razings")
    CUSTOM = (7, "Custom")
