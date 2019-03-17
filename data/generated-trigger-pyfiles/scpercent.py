"""Wrapper for a Starcraft Percent reference.

"""


class SCPercent:
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return self.value


DIGITS_5 = SCPercent('5')
DIGITS_70 = SCPercent('70')
