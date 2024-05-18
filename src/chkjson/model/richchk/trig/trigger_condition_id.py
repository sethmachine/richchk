"""Represent the condition byte of each trigger.

From: http://www.staredit.net/wiki/index.php/Scenario.chk#Trigger_Conditions_List

0 = No Condition

1 = Countdown Timer(Comparison, QNumber)

2 = Command(Player, Comparison, TUnit, QNumber)

3 = Bring(Player, Comparison, TUnit, Loc, QNumber)

4 = Accumulate(Player, Comparison, QNumber, ResType)

5 = Kill(Player, Comparison, TUnit, QNumber)

6 = Command the Most(TUnit)

7 = Commands the Most At(TUnit, Loc)

8 = Most Kills(TUnit)

9 = Highest Score(Score)

10 = Most Resources(ResType)

11 = Switch(Switch)

12 = Elapsed Time(Comparison, QNumber)

13 = Data is a Mission Briefing. Conditions are N/A (Same as Never)

14 = Opponents(Player, Comparison, QNumber)

15 = Deaths(Player, Comparison, TUnit, QNumber)

16 = Command the Least(TUnit)

17 = Command the Least At(TUnit, Loc)

18 = Least Kills(TUnit)

19 = Lowest Score(Score)

20 = Least Resources(ResType)

21 = Score(Player, Comparison, Score, QNumber)

22 = Always (Same as No Condition)

23 = Never
"""


from chkjson.model.richchk.richchk_enum import RichChkEnum


class TriggerConditionId(RichChkEnum):
    NO_CONDITION = (0, "NO_CONDITION")
    COUNTDOWN_TIMER = (1, "COUNTDOWN_TIMER")
    COMMAND = (2, "COMMAND")
    BRING = (3, "BRING")
    ACCUMULATE = (4, "ACCUMULATE")
    KILL = (5, "KILL")
    COMMAND_THE_MOST = (6, "COMMAND_THE_MOST")
    COMMANDS_THE_MOST_AT = (7, "COMMANDS_THE_MOST_AT")
    MOST_KILLS = (8, "MOST_KILLS")
    HIGHEST_SCORE = (9, "HIGHEST_SCORE")
    MOST_RESOURCES = (10, "MOST_RESOURCES")
    SWITCH = (11, "SWITCH")
    ELAPSED_TIME = (12, "ELAPSED_TIME")
    DATA_IS_A_MISSION_BRIEFING = (13, "DATA_IS_A_MISSION_BRIEFING")
    OPPONENTS = (14, "OPPONENTS")
    DEATHS = (15, "DEATHS")
    COMMAND_THE_LEAST = (16, "COMMAND_THE_LEAST")
    COMMAND_THE_LEAST_AT = (17, "COMMAND_THE_LEAST_AT")
    LEAST_KILLS = (18, "LEAST_KILLS")
    LOWEST_SCORE = (19, "LOWEST_SCORE")
    LEAST_RESOURCES = (20, "LEAST_RESOURCES")
    SCORE = (21, "SCORE")
    ALWAYS = (22, "ALWAYS")
    NEVER = (23, "NEVER")
