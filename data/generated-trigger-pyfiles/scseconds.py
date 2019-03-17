"""Wrapper for a Starcraft Seconds reference.

"""


class SCSeconds:
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return self.value


DIGITS_90 = SCSeconds('90')
