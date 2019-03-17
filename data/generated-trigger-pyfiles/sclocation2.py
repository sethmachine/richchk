"""Wrapper for a Starcraft Location2 reference.

"""


class SCLocation2:
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return self.value


BOSSARRIVAL = SCLocation2('"BossArrival"')
P_FORCE_UNALLY_LANDING = SCLocation2('"P Force Unally Landing"')
P7OBS = SCLocation2('"P7Obs"')
P8OBS = SCLocation2('"P8Obs"')
