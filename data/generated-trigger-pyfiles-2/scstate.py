"""Wrapper for a Starcraft State reference.

"""


class SCState:
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return self.value


DISABLED = SCState('disabled')
ENABLED = SCState('enabled')
NOT_SET = SCState('not set')
