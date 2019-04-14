"""Tests all class methods in the chkedit.ChkEdit object for high level editing of a map's CHK data.

"""

import json
import logging
import os
import shutil
import tempfile
import unittest
import unittest.mock

from src.chkjson import chkedit
from src.chkjson import semver

RESOURCES_DIR = os.path.join('resources/chkedit')
BASE_MAPFILE = os.path.join(RESOURCES_DIR, 'demon_lore_yatapi_test.scx')
BASE_CHKFILE = os.path.join(RESOURCES_DIR, 'demon_lore_yatapi_test.chk')
UPDATED_CHKFILE = os.path.join(RESOURCES_DIR, 'demon_lore_yatapi_test_update.chk')


class TestChkEdit(unittest.TestCase):
    def test_extract_chk(self):
        editor = chkedit.ChkEdit()
        with tempfile.NamedTemporaryFile() as tp:
            editor.extract_chk(BASE_MAPFILE, tp.name)
            self.assertEqual(os.path.exists(tp.name), True)
            with open(BASE_CHKFILE, 'rb') as f:
                self.assertEqual(tp.read(), f.read())

    def test_add_chkfile_to_map(self):
        editor = chkedit.ChkEdit()
        with tempfile.NamedTemporaryFile() as tp:
            shutil.copyfile(BASE_MAPFILE, tp.name)
            success = editor.add_chkfile_to_map(UPDATED_CHKFILE, tp.name)
            self.assertEqual(success, True)
            with tempfile.NamedTemporaryFile() as tp2:
                editor.extract_chk(tp.name, tp2.name)
                with open(UPDATED_CHKFILE, 'rb') as f:
                    self.assertEqual(tp2.read(), f.read())
                with open(BASE_CHKFILE, 'rb') as f:
                    self.assertNotEqual(tp2.read(), f.read())

    def test_add_chk_to_map(self):
        editor = chkedit.ChkEdit()
        # mock a chk object that returns the binary chk data when calling .compile() method
        chk = unittest.mock.Mock()
        with open(UPDATED_CHKFILE, 'rb') as f:
            chkdata = f.read()
            chk.compile.return_value = chkdata
        with tempfile.NamedTemporaryFile() as tp:
            shutil.copyfile(BASE_MAPFILE, tp.name)
            success = editor.add_chk_to_map(chk, tp.name)
            self.assertEqual(success, True)
            with tempfile.NamedTemporaryFile() as tp2:
                editor.extract_chk(tp.name, tp2.name)
                with open(UPDATED_CHKFILE, 'rb') as f:
                    self.assertEqual(tp2.read(), f.read())
                with open(BASE_CHKFILE, 'rb') as f:
                    self.assertNotEqual(tp2.read(), f.read())

    def test_create_release_map_from_chk(self):
        editor = chkedit.ChkEdit()
        chk = unittest.mock.Mock()
        with open(UPDATED_CHKFILE, 'rb') as f:
            chkdata = f.read()
            chk.compile.return_value = chkdata
        with tempfile.NamedTemporaryFile() as release_map:
            success = editor.create_release_map_from_chk(chk, BASE_MAPFILE, release_map.name)
            self.assertEqual(success, True)
            with tempfile.NamedTemporaryFile() as release_chk:
                editor.extract_chk(release_map.name, release_chk.name)
                with open(UPDATED_CHKFILE, 'rb') as f:
                    self.assertEqual(release_chk.read(), f.read())
                with open(BASE_CHKFILE, 'rb') as f:
                    self.assertNotEqual(release_chk.read(), f.read())

    def test_release_map_to_dir_from_chk(self):
        editor = chkedit.ChkEdit()
        chk = unittest.mock.Mock()
        with open(UPDATED_CHKFILE, 'rb') as f:
            chkdata = f.read()
            chk.compile.return_value = chkdata
        with tempfile.TemporaryDirectory() as release_dir:
            versions = [semver.VERSION_NOOP, semver.VERSION_PATCH, semver.VERSION_BALANCE,
                        semver.VERSION_MINOR, semver.VERSION_MAJOR]
            for version in versions:
                updated_mapfile = editor.release_map_to_dir_from_chk(chk, BASE_MAPFILE, release_dir, version_update=version)
                self.assertEqual(os.path.exists(updated_mapfile), True)
                with tempfile.NamedTemporaryFile() as release_chk:
                    editor.extract_chk(updated_mapfile, release_chk.name)
                    with open(UPDATED_CHKFILE, 'rb') as f:
                        self.assertEqual(release_chk.read(), f.read())
                    with open(BASE_CHKFILE, 'rb') as f:
                        self.assertNotEqual(release_chk.read(), f.read())
            self.assertEqual(len(os.listdir(release_dir)), len(versions))


if __name__ == '__main__':
    unittest.main()
