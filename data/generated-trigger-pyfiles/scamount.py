"""Wrapper for a Starcraft Amount reference.

"""


class SCAmount:
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return self.value


DIGITS_109 = SCAmount('109')
DIGITS_110 = SCAmount('110')
DIGITS_149 = SCAmount('149')
DIGITS_15 = SCAmount('15')
DIGITS_150 = SCAmount('150')
DIGITS_1800 = SCAmount('1800')
DIGITS_200 = SCAmount('200')
DIGITS_300 = SCAmount('300')
DIGITS_3000 = SCAmount('3000')
DIGITS_400 = SCAmount('400')
DIGITS_600 = SCAmount('600')
DIGITS_64 = SCAmount('64')
DIGITS_65 = SCAmount('65')
DIGITS_700 = SCAmount('700')
DIGITS_74 = SCAmount('74')
DIGITS_75 = SCAmount('75')
DIGITS_800 = SCAmount('800')
DIGITS_84 = SCAmount('84')
DIGITS_85 = SCAmount('85')
DIGITS_900 = SCAmount('900')
DIGITS_94 = SCAmount('94')
DIGITS_95 = SCAmount('95')
