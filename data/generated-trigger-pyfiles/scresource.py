"""Wrapper for a Starcraft Resource reference.

"""


class SCResource:
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return self.value


GAS = SCResource('gas')
ORE = SCResource('ore')
