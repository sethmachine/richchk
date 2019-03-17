"""Wrapper for a Starcraft Title reference.

"""


class SCTitle:
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return self.value


ARMY_SIZE = SCTitle('"Army Size"')
CITIES = SCTitle('"Cities"')
FINAL_SCORE = SCTitle('"Final Score"')
FINAL_SCORES = SCTitle('"Final Scores"')
HOLDINGS = SCTitle('"Holdings"')
X006DAEMON_HEARTS = SCTitle('"\x006Daemon Hearts"')
X006KILLS = SCTitle('"\x006Kills"')
X010SHARDS_OF_AEGIS = SCTitle('"\x010Shards of Aegis"')
X01CTEARS_OF_GARDOS = SCTitle('"\x01cTears of Gardos"')
X01ESAGE_STONES = SCTitle('"\x01eSage Stones"')
