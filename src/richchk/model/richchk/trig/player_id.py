"""ID for each Player/Group.

See: http://www.staredit.net/wiki/index.php/Scenario.chk#List_of_Players.2FGroup_IDs
"""

from ..richchk_enum import RichChkEnum


class PlayerId(RichChkEnum):
    PLAYER_1 = (0, "Player 1")
    PLAYER_2 = (1, "Player 2")
    PLAYER_3 = (2, "Player 3")
    PLAYER_4 = (3, "Player 4")
    PLAYER_5 = (4, "Player 5")
    PLAYER_6 = (5, "Player 6")
    PLAYER_7 = (6, "Player 7")
    PLAYER_8 = (7, "Player 8")
    PLAYER_9 = (8, "Player 9")
    PLAYER_10 = (9, "Player 10")
    PLAYER_11 = (10, "Player 11")
    PLAYER_12 = (11, "Player 12")
    NONE = (12, "None")
    CURRENT_PLAYER = (13, "Current Player")
    FOES = (14, "Foes")
    ALLIES = (15, "Allies")
    NEUTRAL_PLAYERS = (16, "Neutral Players")
    ALL_PLAYERS = (17, "All Players")
    FORCE_1 = (18, "Force 1")
    FORCE_2 = (19, "Force 2")
    FORCE_3 = (20, "Force 3")
    FORCE_4 = (21, "Force 4")
    UNUSED_1 = (22, "Unused 1")
    UNUSED_2 = (23, "Unused 2")
    UNUSED_3 = (24, "Unused 3")
    UNUSED_4 = (25, "Unused 4")
    NON_ALLIED_VICTORY_PLAYERS = (26, "Non Allied Victory Players")
