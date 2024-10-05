"""Unit order.

See: http://www.staredit.net/wiki/index.php/Scenario.chk#Unit_Orders
"""

from .....model.richchk.richchk_enum import RichChkEnum


class UnitOrder(RichChkEnum):
    MOVE = (0, "Move")
    PATROL = (1, "Patrol")
    ATTACK = (2, "Attack")
