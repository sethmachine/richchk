"""Modify or replace the CHK data in .scx/.scm files for programmatic custom map editing.

"""

import os
import shutil
import tempfile
import uuid

import pyw3x.archive

from .chk import Chk
from . import fileutils
from . import logger
from . import semver

CHK_MPQ_PATH = 'staredit\\scenario.chk'
CHK_EXTENSION = '.chk'


class ChkEdit:
    log = logger.get_log("ChkEdit")

    def __init__(self):
        pass

    @classmethod
    def extract_chk(cls, infile, outfile=None) -> str:
        """Extracts the CHK file from a .scx/.scm Starcraft map file.

        :param infile: path to a .scx/.scm Starcraft scenario map file
        :param outfile: where to write extracted CHK data ; if None, uses the basename of the infile
                        plus the .chk extension
        :return: path to the extracted CHK data as a file
        """
        if not outfile:
            outdir = os.path.dirname(infile)
            bn = os.path.basename(infile)
            name, ext = os.path.splitext(bn)
            outfile = os.path.join(outdir, name + CHK_EXTENSION)
        with pyw3x.archive.open_archive(infile, 'r') as a:
            a.extract_file(CHK_MPQ_PATH, outfile)
        return outfile

    @classmethod
    def add_chkfile_to_map(cls, chkfile: str, mapfile: str) -> bool:
        """Replaces the CHK file in the .scx/.scm map file with the new CHK file.

        The archive is also compacted, potentially reducing total map file size.

        :param chkfile: path to extracted CHK file
        :param mapfile: path to a .scx/.scm Starcraft map file
        :return: True if the CHK is added, False otherwise
        """
        with pyw3x.archive.open_archive(mapfile, mode='w') as a:
            success = a.add_file(chkfile, CHK_MPQ_PATH, True)
            a.compact(listfile=None)
            return success

    @classmethod
    def add_chk_to_map(cls, chk: Chk, mapfile: str) -> bool:
        """Compiles the Chk object and replaces the CHK file in the map file

        The output of `chk.compile()` (CHK binary data) is written to a temporary file on disk,
        before being added to the archive (map file).

        :param chk: a Chk object that compiles to the binary CHK format
        :param mapfile: path to a .scx/.scm Starcraft map file
        :return: True if the CHK is added, False otherwise
        """
        with tempfile.NamedTemporaryFile(mode='wb') as tp:
            chkfile = tp.name
            chkdata = chk.compile()
            tp.write(chkdata)
            return cls.add_chkfile_to_map(chkfile, mapfile)

    @classmethod
    def create_release_map_from_chk(cls, chk: Chk, base_mapfile: str, release_mapfile: str):
        """Creates a new release for an existing map by updating its CHK.

        A copy of the base map file is created and its CHK is replaced with the
        output of `chk.compile()`.

        :param chk: a Chk object that compiles to the binary CHK format
        :param base_mapfile: the map to create the release from with the updated CHK data
        :param release_mapfile: copy of the base map but CHK contents replaced with the new CHK data
        :return:
        """
        shutil.copyfile(base_mapfile, release_mapfile)
        return cls.add_chk_to_map(chk, release_mapfile)

    @classmethod
    def release_map_to_dir_from_chk(cls, chk: Chk, base_mapfile: str, release_dir: str, version_update=semver.VERSION_NOOP):
        """Creates a new semantic versioned release in the release directory for an existing map by updating its CHK.

        A copy of the base map file is created and its CHK is replaced with the
        output of `chk.compile()`.

        :param chk: a Chk object that compiles to the binary CHK format
        :param base_mapfile: the map to create the release from with the updated CHK data
        :param release_dir: directory to create the release with updated CHK data;
                            will create the directory if it does not exist
        :param version_update: one of 'major', 'minor', 'patch', 'balance', or 'noop'
        :return:
        """
        if not os.path.exists(release_dir):
            cls.log.info('Creating release directory because it does not exist: {}'.format(release_dir))
            os.mkdir(release_dir)
        updated_mapfile = semver.write_next_version(base_mapfile, release_dir, version_update)
        cls.log.info('Updated mapfile: {}'.format(updated_mapfile))
        success = cls.add_chk_to_map(chk, updated_mapfile)
        if success:
            cls.log.info('Successfully updated {} with  CHK data'.format(updated_mapfile))
        else:
            cls.log.error('Failed to update {} with CHK data'.format(updated_mapfile))
        return updated_mapfile


if __name__ == '__main__':
    pass
