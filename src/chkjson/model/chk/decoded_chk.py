"""Represents the ordered list of decoded CHK sections from a decoded CHK file.

"""

import dataclasses

from chkjson.model.chk.decoded_chk_section import DecodedChkSection


@dataclasses.dataclass(frozen=True)
class DecodedChk:
    decoded_chk_sections: list[DecodedChkSection]


if __name__ == "__main__":
    pass
