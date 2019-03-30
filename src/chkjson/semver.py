"""Implementation of semantic versioning with 4 parts: major, minor, patch, and balance.

See: https://semver.org/

"""

import dataclasses
import os
import shutil
import re

from . import fileutils

VERSION_PREFIX = '-v'
VERSION_ONE = '{}0.0.0.0'.format(VERSION_PREFIX)
VERSION_REGEX = re.compile(r'{}(?P<major>[0-9]+)\.(?P<minor>[0-9]+)\.(?P<patch>[0-9]+)\.(?P<balance>[0-9]+)'.
                           format(VERSION_PREFIX))
VERSION_MAJOR = 'major'
VERSION_MINOR = 'minor'
VERSION_PATCH = 'patch'
VERSION_BALANCE = 'balance'
VERSION_NOOP = 'noop'


@dataclasses.dataclass
class Version:
    """Semantic versioning when releasing new maps.

    A version consists of 4 parts:
    major.minor.patch.balance, e.g. 12.13.2.15

    When major version is incremented, all other versions are reset to 0.
    When minor version is incremented, patch and balance versions are reset to 0.
    Incrementing patch or balance does not change any other versions, e.g.:

    0.0.13.2 + patch -> 0.0.14.2
    0.0.13.2 + balance -> 0.0.13.3

    major: when you make incompatible API changes
    minor: when you add functionality in a backwards-compatible manner
    patch: when you make backwards-compatible bug fixes
    balance: when altering costs, unit stats, terrain, etc.

    """
    prefix = VERSION_PREFIX
    major: int
    minor: int
    patch: int
    balance: int

    def to_string(self):
        return '{}{}.{}.{}.{}'.format(self.prefix, self.major, self.minor, self.patch, self.balance)

    def __repr__(self):
        return self.to_string()

    def increment(self, update: str = VERSION_NOOP):
        """Increments the version according to the version update.

        Five possible updates:
        'major', 'minor', 'patch', 'balance', or 'noop'

        'noop' does no incrementing.

        :param update: one of 'major', 'minor', 'patch', 'balance', or 'noop'
        :return:
        """
        if update == VERSION_NOOP:
            pass
        elif update == VERSION_MAJOR:
            self.major += 1
            self.minor = 0
            self.patch = 0
            self.balance = 0
        elif update == VERSION_MINOR:
            self.minor += 1
            self.patch = 0
            self.balance = 0
        elif update == VERSION_PATCH:
            self.patch += 1
        elif update == VERSION_BALANCE:
            self.balance += 1

    @classmethod
    def from_string(cls, string_):
        match = VERSION_REGEX.search(string_)
        return cls(major=int(match.group('major')), minor=int(match.group('minor')), patch=int(match.group('patch')),
                   balance=int(match.group('balance')))

    def __gt__(self, other):
        if self.major > other.major:
            return True
        elif self.major < other.major:
            return False
        else:
            if self.minor > other.minor:
                return True
            elif self.minor < other.minor:
                return False
            else:
                if (self.patch + self.balance) >= (other.patch + other.balance):
                    return True
                else:
                    return False


def get_latest_version(infile, outdir):
    bn = os.path.basename(infile)
    name, ext = os.path.splitext(bn)
    # grab all versions then sort by highest and increment
    regex = re.compile(r'{}{}[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+{}'.format(name, '-v', '\\.{}'.format(ext.replace('.', ''))))
    versions = [Version.from_string(os.path.basename(path)) for path in fileutils.absolute_filepaths(outdir, 0, regex)]
    versions.sort(reverse=True)
    latest = versions[0]
    return latest


def get_next_version(infile: str, outdir: str, update=VERSION_NOOP, prefix=VERSION_PREFIX):
    """Generates the name of the next version of the file based on existing versions in the same directory.

    See Semantic Versioning: https://semver.org/

    :param infile: the updated versioned name of the new file to write to
    :return:
    """
    bn = os.path.basename(infile)
    name, ext = os.path.splitext(bn)
    # grab all versions then sort by highest and increment
    regex = re.compile(r'{}{}[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+{}'.format(name, '-v', '\.{}'.format(ext.replace('.', ''))))
    versions = [Version.from_string(os.path.basename(path)) for path in fileutils.absolute_filepaths(outdir, 0, regex)]
    if not versions:
        return os.path.join(outdir, name + VERSION_ONE + ext)
    else:
        versions.sort(reverse=True)
        latest = versions[0]
        latest.increment(update)
        return os.path.join(outdir, name + latest.to_string() + ext)


def write_next_version(infile, outdir, update=VERSION_NOOP, prefix=VERSION_PREFIX):
    next_ = get_next_version(infile, outdir, update, prefix)
    shutil.copyfile(infile, next_)
    return next_


if __name__ == '__main__':
    pass
