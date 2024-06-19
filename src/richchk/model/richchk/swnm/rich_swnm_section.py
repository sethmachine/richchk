"""SWNM - Switch names.

Contains only Switches which are have a custom name and/or are used in at least 1
condition or action.
"""
import dataclasses

from ...chk_section_name import ChkSectionName
from ..rich_chk_section import RichChkSection
from .rich_switch import RichSwitch


@dataclasses.dataclass(frozen=True)
class RichSwnmSection(RichChkSection):

    _switches: list[RichSwitch]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.SWNM

    @property
    def switches(self) -> list[RichSwitch]:
        return self._switches
