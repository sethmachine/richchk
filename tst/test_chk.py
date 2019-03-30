"""

"""

import json
import logging
import unittest

from src import chkjson
from chkjson.chk import Chk, ChkReader

CHKFILE = 'resources/chk/demon_lore_yatapi_test.chk'
with open(CHKFILE, 'rb') as f:
    CHKDATA = f.read()
# CHKJSON = json.load(open('resources/chkunix/chkunix.json', 'r'))


class TestChk(unittest.TestCase):
    def test_decompile_compile(self):
        reader = ChkReader()
        chk = reader.read(CHKFILE)
        self.assertEqual(chk.compile(), CHKDATA)


if __name__ == '__main__':
    unittest.main()
