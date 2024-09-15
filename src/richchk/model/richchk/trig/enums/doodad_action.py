"""Trigger action state.

Use this to disable/enable doodad units (like gates, floor traps, etc.).

See:
http://www.staredit.net/wiki/index.php/Scenario.chk#Action_States
"""

from .....model.richchk.richchk_enum import RichChkEnum


class DoodadAction(RichChkEnum):
    SET = (4, "Enable")
    CLEAR = (5, "Disable")
    TOGGLE = (6, "Toggle")
