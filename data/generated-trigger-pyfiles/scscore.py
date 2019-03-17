"""Wrapper for a Starcraft Score reference.

"""


class SCScore:
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return self.value


CUSTOM = SCScore('Custom')
