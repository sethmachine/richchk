"""Force slot identifiers as used in the FORC section.

See:
http://staredit.net/wiki/index.php/Scenario.chk#.22FORC.22_-_Force_Settings
"""

from ....model.richchk.richchk_enum import RichChkEnum


class ForceId(RichChkEnum):
    FORCE_1 = (0, "Force 1")
    FORCE_2 = (1, "Force 2")
    FORCE_3 = (2, "Force 3")
    FORCE_4 = (3, "Force 4")
