"""Switch states.

See: http://www.staredit.net/wiki/index.php/Scenario.chk#Switch_States
"""

from chkjson.model.richchk.richchk_enum import RichChkEnum


class SwitchState(RichChkEnum):
    SET = (2, "Switch is set")
    CLEARED = (3, "Switch is cleared")
