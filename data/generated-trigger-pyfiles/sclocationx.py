"""Wrapper for a Starcraft Locationx reference.

"""


class SCLocationx:
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return self.value


P1OBSCENTER = SCLocationx('"P1ObsCenter"')
P2EXIT = SCLocationx('"P2Exit"')
P2MOUTH = SCLocationx('"P2Mouth"')
P2OBSCENTER = SCLocationx('"P2ObsCenter"')
P3EXIT = SCLocationx('"P3Exit"')
P3MOUTH = SCLocationx('"P3Mouth"')
P3OBSCENTER = SCLocationx('"P3ObsCenter"')
P4EXIT = SCLocationx('"P4Exit"')
P4MOUTH = SCLocationx('"P4Mouth"')
P4OBSCENTER = SCLocationx('"P4ObsCenter"')
P5EXIT = SCLocationx('"P5Exit"')
P5MOUTH = SCLocationx('"P5Mouth"')
P5OBSCENTER = SCLocationx('"P5ObsCenter"')
P6EXIT = SCLocationx('"P6Exit"')
P6MOUTH = SCLocationx('"P6Mouth"')
P6OBSCENTER = SCLocationx('"P6ObsCenter"')
