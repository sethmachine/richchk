"""Player controller types as used in the OWNR section.

See:
http://staredit.net/wiki/index.php/Scenario.chk#.22OWNR.22_-_StarCraft_Player_Types
"""

from ....model.richchk.richchk_enum import RichChkEnum


class PlayerController(RichChkEnum):
    INACTIVE = (0x00, "Inactive")
    COMPUTER_GAME = (0x01, "Computer (game)")
    HUMAN_OCCUPIED = (0x02, "Occupied by Human Player")
    RESCUE_PASSIVE = (0x03, "Rescue Passive")
    UNUSED = (0x04, "Unused")
    COMPUTER = (0x05, "Computer")
    HUMAN = (0x06, "Human (Open Slot)")
    NEUTRAL = (0x07, "Neutral")
    CLOSED = (0x08, "Closed Slot")
