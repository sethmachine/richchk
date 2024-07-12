"""Enable, disable, or toggle showing computers in leaderboards.

See: http://www.staredit.net/wiki/index.php/Scenario.chk#Action_States
"""

from .....model.richchk.richchk_enum import RichChkEnum


class ComputerLeaderboardAction(RichChkEnum):
    SET = (4, "Show Computer players in Leaderboard")
    CLEAR = (5, "Hide Computer players in Leaderboard")
    TOGGLE = (6, "Toggle Computer players in Leaderboard")
