"""Alliance status.

See: http://www.staredit.net/wiki/index.php/Scenario.chk#Alliance_Statuses
"""

from .....model.richchk.richchk_enum import RichChkEnum


class AllianceStatus(RichChkEnum):
    ENEMY = (0, "Enemy")
    ALLY = (1, "Ally")
    ALLIED_VICTORY = (2, "Allied Victory")
