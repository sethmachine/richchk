"""Trigger action state.

Use this to disable/enable unit invincibility.

See:
http://www.staredit.net/wiki/index.php/Scenario.chk#Action_States
"""

from .....model.richchk.richchk_enum import RichChkEnum


class Invincibility(RichChkEnum):
    SET = (4, "Enable")
    CLEAR = (5, "Disable")
    TOGGLE = (6, "Toggle")
