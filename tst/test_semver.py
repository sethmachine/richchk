"""

"""

import os
import tempfile
import unittest

from src.chkjson import semver

CHKFILE = 'resources/semver/demon_lore_yatapi_test_update.chk'


class TestSemver(unittest.TestCase):
    def test_equality(self):
        """Tests to compare versions to determine which are newest.

        :return:
        """
        a = semver.Version(1, 0, 0, 0)
        b = semver.Version(0, 0, 0, 0)
        self.assertGreater(a, b)
        self.assertLess(b, a)
        a = semver.Version(1, 2, 0, 0)
        b = semver.Version(1, 1, 0, 0)
        self.assertGreater(a, b)
        self.assertLess(b, a)
        a = semver.Version(5, 5, 1, 0)
        b = semver.Version(5, 5, 0, 0)
        self.assertGreater(a, b)
        self.assertLess(b, a)
        a = semver.Version(5, 5, 5, 3)
        b = semver.Version(5, 5, 5, 2)
        self.assertGreater(a, b)
        self.assertLess(b, a)
        a = semver.Version(5, 5, 3, 10)
        b = semver.Version(5, 5, 5, 2)
        self.assertGreater(a, b)
        self.assertLess(b, a)

    def test_increment_version(self):
        """Tests to increment different versions (major, minor, patch, balance, noop) and observe appropriate effects.

        :return:
        """
        a = semver.Version(0, 0, 0, 0)
        a.increment(semver.VERSION_MAJOR)
        self.assertEqual(a.major, 1)
        a.increment(semver.VERSION_MINOR)
        self.assertEqual(a.minor, 1)
        a.increment(semver.VERSION_PATCH)
        self.assertEqual(a.patch, 1)
        a.increment(semver.VERSION_BALANCE)
        self.assertEqual(a.balance, 1)
        a.increment(semver.VERSION_NOOP)
        self.assertEqual(a, semver.Version(1, 1, 1, 1))

    def test_write_and_get_next_version(self):
        """Tests writing a bunch of incremented versions and getting the last expected latest version.

        :return:
        """
        with tempfile.TemporaryDirectory() as outdir:
            semver.write_next_version(CHKFILE, outdir, update=semver.VERSION_MINOR)
            semver.write_next_version(CHKFILE, outdir, update=semver.VERSION_BALANCE)
            semver.write_next_version(CHKFILE, outdir, update=semver.VERSION_BALANCE)
            semver.write_next_version(CHKFILE, outdir, update=semver.VERSION_BALANCE)
            semver.write_next_version(CHKFILE, outdir, update=semver.VERSION_PATCH)
            semver.write_next_version(CHKFILE, outdir, update=semver.VERSION_MINOR)
            semver.write_next_version(CHKFILE, outdir, update=semver.VERSION_MAJOR)
            semver.write_next_version(CHKFILE, outdir, update=semver.VERSION_MINOR)
            semver.write_next_version(CHKFILE, outdir, update=semver.VERSION_MINOR)
            semver.write_next_version(CHKFILE, outdir, update=semver.VERSION_BALANCE)
            semver.write_next_version(CHKFILE, outdir, update=semver.VERSION_PATCH)
            semver.write_next_version(CHKFILE, outdir, update=semver.VERSION_MAJOR)
            semver.write_next_version(CHKFILE, outdir, update=semver.VERSION_BALANCE)
            final = semver.write_next_version(CHKFILE, outdir, update=semver.VERSION_PATCH)
            print(outdir, final)
            print(os.listdir(outdir))
            latest = semver.get_latest_version(CHKFILE, outdir)
            expected_latest = semver.Version(2, 0, 1, 1)
            self.assertEqual(latest, expected_latest)


if __name__ == '__main__':
    unittest.main()
