"""Implements the CHK format, providing a parser to decompile CHK to JSON and compile JSON to CHK.

See: http://www.starcraftai.com/wiki/CHK_Format

"""

import collections
import dataclasses
import os
import struct
import typing

from . import logger
from .section.abstract_chksection import ChkSection
from .section.chkunk import ChkUnk
from .section.name2section import name2section


@dataclasses.dataclass
class Chk:
    sections: typing.List[ChkSection]
    name2sections: typing.Dict[str, typing.List[ChkSection]]

    def get_sections(self, name) -> typing.List[ChkSection]:
        return self.name2sections.get(name)

    def decompile(self, data: bytes):
        pass

    def compile(self, data: typing.Dict):
        pass


class ChkReader:
    def __init__(self):
        self.log = logger.get_log(ChkReader.__name__)

    def read(self, chkfile: str) -> Chk:
        """Reads the binary CHK file into Python objects.

        From: http://www.starcraftai.com/wiki/CHK_Format#Sections

        The CHK is split into several named chunks (hence the file extension, an abbreviation of CHunK).

        Each section begins with an 8-byte header:

        u32 Name - A 4-byte string uniquely identifying that chunk's purpose.
        u32 Size - The size, in bytes, of the chunk (not including this header)
        Followed by as many bytes as 'Size', in a format described below.

        Some things to keep in mind about the CHK section:

        Invalid sections can exist and will be ignored. While Size is unsigned, it can safely be a negative value
        to read a chunk earlier in the file. This allows for "section stacking", allowing smaller sections to be placed
        inside of larger ones or duplicate triggers or units to take less space in the file.
        All sections will marked "Not required." are never read by StarCraft and can safely be omitted. However
        they may or may not be read by StarEdit, and may cause the map to be unreadable in an editor.
        Note "Hybrid", or "Enhanced", maps were introduced in 1.04. They are supported both by Original StarCraft
        and Brood War and usually contain sections for both types (e.g., UPGS and UPGx, TECS and TECx),
        but both sections aren't necessarily read.
        Duplicate sections will overwrite previously defined section data, except where noted. Note this only applies
        to those section that pass the specified "validation" parameters, as any section that does not successfully validate will be ignored

        :param chkfile:
        :return:
        """
        sections = []
        name2sections = collections.defaultdict(list)
        with open(chkfile, 'rb') as f:
            while True:
                name_bytes = f.read(4)
                if name_bytes == b'':
                    break
                # read name, size
                # u32 Name - A 4-byte string uniquely identifying that chunk's purpose.
                name = struct.unpack('4s', name_bytes)[0].decode('utf-8')
                # u32 Size - The size, in bytes, of the chunk (not including this header)
                size = struct.unpack('I', f.read(4))[0]
                section_data = f.read(size)
                section_class = name2section(name)
                if section_class is ChkUnk:
                    self.log.warning('Unknown section: {}'.format(name))
                    sect = section_class.decompile(section_data)
                    sect.name = name
                else:
                    sect = section_class.decompile(section_data)
                sect.data = section_data
                sections.append(sect)
                name2sections[name].append(sect)
        return Chk(sections=sections, name2sections=name2sections)


class ChkWriter:
    def __init__(self):
        pass

    def write(self, chk: Chk, outfile: str):
        """Writes the Chk object and its sections to the binary CHK format.

        :param chk:
        :param outfile:
        :return:
        """
        pass


def save_sections_to_dir(sections: typing.List[ChkSection], outdir: str):
    """Saves each CHK section to its own file for debugging.

    :param sections:
    :param outdir:
    :return:
    """
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    for sect in sections:
        if isinstance(sect, ChkUnk):
            name = sect.name
        else:
            name = sect.__class__.name
        outfile = os.path.join(outdir, '{}.{}'.format(name, name.lower().strip()))
        with open(outfile, 'wb') as f:
            f.write(sect.data)



if __name__ == '__main__':
    infile = '../../data/chk/demon_lore_yatapi_test.chk'
    chkr = ChkReader()
    c = chkr.read(infile)
    save_sections_to_dir(c.sections, '../../data/chk-sections')
    z = c.get_sections('STR ')[0]
    od = z.data
    # a = z.compile(header=False)
    # # z.add_string('addme')
    # print(z.get_index('Nexus1'))
    # idx = z.remove_string('Nexus2')
    # z.syncdata()
    # print(z.get_index('Nexus1'))
    # d = z.compile(header=False)
