"""

"""

from chkjson.model.chk.chk_section_names import ChkSectionName
from chkjson.model.chk.str.chk_str import ChkStr
from chkjson.parsers.abstract_chk_section_parser import AbstractChkSectionParser


class ChkStrParser(AbstractChkSectionParser[ChkStr]):
    @property
    def chk_section_name(self) -> ChkSectionName:
        return ChkSectionName.STR

    def parse(self, data: bytes) -> ChkStr:
        return None

    def compile(self, chk_section: ChkStr) -> bytes:
        return b""


if __name__ == "__main__":
    pass
