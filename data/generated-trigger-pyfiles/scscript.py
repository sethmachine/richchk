"""Wrapper for a Starcraft Script reference.

"""


class SCScript:
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return self.value


VI6 = SCScript('"+Vi6"')
VI7 = SCScript('"+Vi7"')
JYDG = SCScript('"JYDg"')
