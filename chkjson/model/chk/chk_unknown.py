"""Represents unknown or unparsed CHK sections.

This CHK section is not formerly part of the CHK specification and instead is used to handle
any internal parsing issues.




"""

import dataclasses

from chkjson.model.chk.base_chk_section import BaseChkSection


@dataclasses.dataclass
class ChkUnknown(BaseChkSection):
    raw_name: str
