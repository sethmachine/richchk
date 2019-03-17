"""Wrapper for a Starcraft Alliance reference.

"""


class SCAlliance:
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return self.value


ALLIED_VICTORY = SCAlliance('Allied Victory')
ALLY = SCAlliance('Ally')
ENEMY = SCAlliance('Enemy')
