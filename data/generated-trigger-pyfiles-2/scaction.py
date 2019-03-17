"""Wrapper for a Starcraft Action reference.

"""


class SCAction:
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return self.value


CLEAR = SCAction('clear')
RANDOMIZE = SCAction('randomize')
SET = SCAction('set')
TOGGLE = SCAction('toggle')
