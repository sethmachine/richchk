"""

"""

import json
import logging
import unittest

from src import chkjson
from chkjson.section.chkstr import ChkStr

STR_SECTION = 'resources/chkstr/STR .str'
with open(STR_SECTION, 'rb') as f:
    STR_DATA = f.read()
STR_JSON = json.load(open('resources/chkstr/str.json', 'r'))


class TestChkStr(unittest.TestCase):
    def test_decompile(self):
        chk = ChkStr.decompile(STR_DATA)
        self.assertEqual(chk.num_strings, STR_JSON['num_strings'])
        self.assertEqual(chk.string_offsets, STR_JSON['string_offsets'])
        self.assertEqual(chk.strings, STR_JSON['strings'])

    def test_compile(self):
        chk = ChkStr.decompile(STR_DATA)
        data = chk.compile(header=False)
        self.assertEqual(data, STR_DATA)

    def test_offsets(self):
        """Confirms that each string offset maps to each string correctly.

        To get the string from the binary data use this formula.

        start = offsets[string]
        end = start + len(string)
        string == data[start: end]

        :return:
        """
        chk = ChkStr.decompile(STR_DATA)
        chk.data = STR_DATA
        for i, offset in enumerate(chk.string_offsets):
            start = offset
            end = offset + len(chk.strings[i])
            self.assertEqual(chk.strings[i], chk.data[start: end].decode('utf-8'))

    def test_add_string_already_exists(self):
        chk = ChkStr.decompile(STR_DATA)
        chk.log.setLevel(logging.ERROR)
        chk.data = STR_DATA
        addme = 'Untitled Scenario'
        self.assertEqual(chk.add_string(addme), False)
        self.assertEqual(chk.syncdata(), False)

    def test_add_string(self):
        chk = ChkStr.decompile(STR_DATA)
        chk.data = STR_DATA
        addme = 'addme'
        self.assertEqual(chk.add_string(addme), True)
        self.assertEqual(chk.syncdata(), True)
        self.assertIn(addme, chk.strings)
        self.assertIn(addme, chk.stringset)

    def test_add_string_check_offsets(self):
        chk = ChkStr.decompile(STR_DATA)
        chk.data = STR_DATA
        addme = 'addme'
        self.assertEqual(chk.add_string(addme), True)
        self.assertEqual(chk.syncdata(), True)
        self.assertIn(addme, chk.strings)
        self.assertIn(addme, chk.stringset)
        for i, offset in enumerate(chk.string_offsets):
            start = offset
            end = offset + len(chk.strings[i])
            self.assertEqual(chk.strings[i], chk.data[start: end].decode('utf-8'))

    def test_add_strings_check_offsets(self):
        chk = ChkStr.decompile(STR_DATA)
        chk.data = STR_DATA
        addme = ['addme', 'add me again', 'hello world!!!!']
        for string_ in addme:
            self.assertEqual(chk.add_string(string_), True)
            self.assertEqual(chk.syncdata(), True)
            self.assertIn(string_, chk.strings)
            self.assertIn(string_, chk.stringset)
        for i, offset in enumerate(chk.string_offsets):
            start = offset
            end = offset + len(chk.strings[i])
            self.assertEqual(chk.strings[i], chk.data[start: end].decode('utf-8'))

    def test_add_strings_syncdata(self):
        chk = ChkStr.decompile(STR_DATA)
        chk.data = STR_DATA
        addme = ['addme', 'add me again', 'hello world!!!!']
        for string_ in addme:
            self.assertEqual(chk.add_string(string_), True)
            self.assertEqual(chk.syncdata(), True)
            self.assertIn(string_, chk.strings)
            self.assertIn(string_, chk.stringset)
        nchk = ChkStr.decompile(chk.data)
        nchk.syncdata()
        self.assertEqual(chk.data, nchk.data)
        self.assertEqual(chk.num_strings, nchk.num_strings)
        self.assertEqual(chk.string_offsets, nchk.string_offsets)
        self.assertEqual(chk.strings, nchk.strings)

    def test_remove_string_does_not_exist(self):
        chk = ChkStr.decompile(STR_DATA)
        chk.log.setLevel(logging.ERROR)
        chk.data = STR_DATA
        removeme = 'I dont exist!'
        self.assertEqual(chk.remove_string(removeme), -1)
        self.assertEqual(chk.syncdata(), False)

    def test_removeme_string(self):
        chk = ChkStr.decompile(STR_DATA)
        chk.data = STR_DATA
        removeme = 'Nexus1'
        self.assertNotEqual(chk.remove_string(removeme), -1)
        self.assertEqual(chk.syncdata(), True)
        self.assertNotIn(removeme, chk.strings)
        self.assertNotIn(removeme, chk.stringset)

    def test_remove_string_check_offsets(self):
        chk = ChkStr.decompile(STR_DATA)
        chk.data = STR_DATA
        removeme = 'Nexus1'
        self.assertNotEqual(chk.remove_string(removeme), -1)
        self.assertEqual(chk.syncdata(), True)
        self.assertNotIn(removeme, chk.strings)
        self.assertNotIn(removeme, chk.stringset)
        for i, offset in enumerate(chk.string_offsets):
            start = offset
            end = offset + len(chk.strings[i])
            self.assertEqual(chk.strings[i], chk.data[start: end].decode('utf-8'))

    def test_remove_strings_check_offsets(self):
        chk = ChkStr.decompile(STR_DATA)
        chk.data = STR_DATA
        removeme = ['Nexus1', 'Nexus2', 'Depot1']
        for string_ in removeme:
            self.assertNotEqual(chk.remove_string(string_), -1)
            self.assertEqual(chk.syncdata(), True)
            self.assertNotIn(string_, chk.strings)
            self.assertNotIn(string_, chk.stringset)
        for i, offset in enumerate(chk.string_offsets):
            start = offset
            end = offset + len(chk.strings[i])
            self.assertEqual(chk.strings[i], chk.data[start: end].decode('utf-8'))

    def test_remove_strings_syncdata(self):
        chk = ChkStr.decompile(STR_DATA)
        chk.data = STR_DATA
        removeme = ['Nexus1', 'Nexus2', 'Depot1']
        for string_ in removeme:
            self.assertNotEqual(chk.remove_string(string_), -1)
            self.assertEqual(chk.syncdata(), True)
            self.assertNotIn(string_, chk.strings)
            self.assertNotIn(string_, chk.stringset)
        nchk = ChkStr.decompile(chk.data)
        nchk.syncdata()
        self.assertEqual(chk.data, nchk.data)
        self.assertEqual(chk.num_strings, nchk.num_strings)
        self.assertEqual(chk.string_offsets, nchk.string_offsets)
        self.assertEqual(chk.strings, nchk.strings)


if __name__ == '__main__':
    unittest.main()
