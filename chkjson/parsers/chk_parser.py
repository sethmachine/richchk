"""Read and write CHK format to and from JSON.

"""

import io
import struct
from collections import defaultdict
from typing import Optional

import chkjson.utils.logger
from chkjson.model.chk.base_chk_section import BaseChkSection
from chkjson.model.chk.chk_header import ChkHeader
from chkjson.model.chk.chk_section_names import ChkSectionName
from chkjson.model.chk.chk_unknown import ChkUnknown
from chkjson.parsers.chk_section_parser_registry import ChkSectionParserRegistry
from chkjson.parsers.sections.abstract_chk_section_parser import (
    AbstractChkSectionParser,
)


class ChkParser:
    def __init__(self):
        self._log = chkjson.utils.logger.get_logger(self.__class__.__name__)

    def parse_file(self, chkfile: str) -> dict[str, list[BaseChkSection]]:
        """Parse a CHK file into JSON serializable objects.

        :param chkfile: absolute path to a complete CHK file
        :return:
        """
        with open(chkfile, "rb") as f:
            return self.parse_bytes(f.read())

    def parse_bytes(self, data: bytes) -> dict[str, list[BaseChkSection]]:
        """Parse CHK bytes into JSON serializable objects.

        :param data: entire bytes representing a complete CHK file.
        :return:
        """
        byte_stream = io.BytesIO(data)
        sections = defaultdict(list)
        chk_header = self._parse_header(byte_stream)
        while chk_header:
            chk_section_data = byte_stream.read(chk_header.size_in_bytes)
            sections[chk_header.name.value].append(
                self._parse_section(chk_header, chk_section_data)
            )
            chk_header = self._parse_header(byte_stream)
        return dict(sections)

    def _parse_header(self, byte_stream: io.BytesIO) -> Optional[ChkHeader]:
        # u32 Name - A 4-byte string uniquely identifying that chunk's purpose.
        chk_section_name_bytes = byte_stream.read(4)
        if chk_section_name_bytes == b"":
            return None
        raw_name = struct.unpack("4s", chk_section_name_bytes)[0].decode("utf-8")
        # u32 Size - The size, in bytes, of the chunk (not including this header)
        chk_section_size = struct.unpack("I", byte_stream.read(4))[0]
        if ChkSectionName.contains(raw_name):
            chk_section_name = ChkSectionName.get_by_value(raw_name)
        else:
            chk_section_name = ChkSectionName.UNKNOWN
            self._log.warning(
                "Unknown/unhandled CHK section: name: {}, size in bytes: {}".format(
                    raw_name, chk_section_size
                )
            )
        return ChkHeader(chk_section_name, raw_name, chk_section_size)

    def _parse_section(self, chk_header: ChkHeader, data: bytes) -> BaseChkSection:
        if chk_header.name == ChkSectionName.UNKNOWN:
            return ChkUnknown(chk_header.name, data, chk_header.raw_name)
        if not ChkSectionParserRegistry.contains(chk_header.name):
            self._log.error(
                "No parser exists for CHK section: name: {}.  "
                "Did we forget to add one to ChkSectionParserRegistry?  "
                "Defaulting to ChkUnknown.".format(chk_header.raw_name)
            )
            return ChkUnknown(chk_header.name, data, chk_header.raw_name)
        parser: AbstractChkSectionParser = (
            ChkSectionParserRegistry.get_by_chk_section_name(chk_header.name)()
        )
        self._log.info(
            "FOUND SECTION: {}.  Size: {}".format(
                chk_header.name, chk_header.size_in_bytes
            )
        )
        return parser.parse(data)


if __name__ == "__main__":
    from chkjson.parsers.sections.chk_str_parser import ChkStrParser

    cp = ChkParser()
    infile = "/Users/sdworman/Desktop/projects/personal/chkjson/data/chk/demon_lore_yatapi_test.chk"
    s = cp.parse_file(infile)
    st = s.get("STR ")[0]
    sp = ChkStrParser()
