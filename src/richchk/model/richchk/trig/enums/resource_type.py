"""Resource type.

See: http://www.staredit.net/wiki/index.php/Scenario.chk#Resource_Types
"""

from .....model.richchk.richchk_enum import RichChkEnum


class ResourceType(RichChkEnum):
    ORE = (0, "Ore")
    GAS = (1, "Gas")
    ORE_AND_GAS = (2, "Ore and Gas")
