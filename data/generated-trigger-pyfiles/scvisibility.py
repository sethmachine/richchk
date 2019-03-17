"""Wrapper for a Starcraft Visibility reference.

"""


class SCVisibility:
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return self.value


ALWAYS_DISPLAY = SCVisibility('Always Display')
