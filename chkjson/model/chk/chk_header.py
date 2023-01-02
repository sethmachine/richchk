"""

"""

from dataclasses import dataclass

from chkjson.model.chk.chk_section_names import ChkSectionName


@dataclass
class ChkHeader:
    name: ChkSectionName
    raw_name: str
    size_in_bytes: int
