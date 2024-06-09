"""Switch action.

See: http://www.staredit.net/wiki/index.php/Scenario.chk#Action_States
"""

from .....model.richchk.richchk_enum import RichChkEnum


class SwitchAction(RichChkEnum):
    SET = (4, "Set/Enable switch")
    CLEAR = (5, "Clear/Disable switch")
    TOGGLE = (6, "Toggle switch")
    RANDOMIZE = (11, "Randomize switch")
