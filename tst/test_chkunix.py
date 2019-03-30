"""

"""

import json
import logging
import unittest

from src import chkjson
from chkjson.section.chkunix import ChkUnix

CHK_SECTION = 'resources/chkunix/UNIx.unix'
with open(CHK_SECTION, 'rb') as f:
    CHKDATA = f.read()
CHKJSON = json.load(open('resources/chkunix/chkunix.json', 'r'))


class TestChkUnix(unittest.TestCase):
    def test_decompile(self):
        chk = ChkUnix.decompile(CHKDATA)
        for key in CHKJSON:
            val = getattr(chk, key)
            self.assertEqual(val, CHKJSON[key])

    def test_compile(self):
        chk = ChkUnix.decompile(CHKDATA)
        data = chk.compile(header=False)
        self.assertEqual(data, CHKDATA)


if __name__ == '__main__':
    unittest.main()
