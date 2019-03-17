"""Wrapper for a Starcraft Milliseconds reference.

"""


class SCMilliseconds:
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return self.value


DIGITS_0 = SCMilliseconds('0')
DIGITS_10000 = SCMilliseconds('10000')
DIGITS_12000 = SCMilliseconds('12000')
DIGITS_15000 = SCMilliseconds('15000')
DIGITS_17000 = SCMilliseconds('17000')
DIGITS_18000 = SCMilliseconds('18000')
DIGITS_20000 = SCMilliseconds('20000')
DIGITS_25000 = SCMilliseconds('25000')
DIGITS_6000 = SCMilliseconds('6000')
DIGITS_8000 = SCMilliseconds('8000')
