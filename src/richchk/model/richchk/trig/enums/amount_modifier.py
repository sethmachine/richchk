"""Amount modifier.

See: http://www.staredit.net/wiki/index.php/Scenario.chk#Number_Modifiers
"""

from .....model.richchk.richchk_enum import RichChkEnum


class AmountModifier(RichChkEnum):
    SET_TO = (7, "Set to")
    ADD = (8, "Add")
    SUBTRACT = (9, "Subtract")
