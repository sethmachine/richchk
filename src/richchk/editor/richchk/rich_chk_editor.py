"""Replace existing RichChkSections in a RichChk."""

import logging
from typing import Union

from ...model.chk.decoded_chk_section import DecodedChkSection
from ...model.chk_section_name import ChkSectionName
from ...model.richchk.rich_chk import RichChk
from ...model.richchk.rich_chk_section import RichChkSection
from ...util import logger


class RichChkEditor:
    def __init__(self) -> None:
        self.log: logging.Logger = logger.get_logger(RichChkEditor.__name__)

    def replace_chk_section(
        self, new_section: RichChkSection, richchk: RichChk
    ) -> RichChk:
        existing_sections = richchk.chk_sections
        new_sections = self._replace_chk_section(new_section, existing_sections)
        return RichChk(_chk_sections=new_sections)

    def _replace_chk_section(
        self,
        new_section: RichChkSection,
        existing_sections: list[Union[DecodedChkSection, RichChkSection]],
    ) -> list[Union[DecodedChkSection, RichChkSection]]:
        modified_sections: list[Union[DecodedChkSection, RichChkSection]] = []
        section_was_replaced = False
        for section in existing_sections:
            if (
                isinstance(section, RichChkSection)
                and section.section_name() == new_section.section_name()
            ):
                section_was_replaced = True
                modified_sections.append(new_section)
            else:
                modified_sections.append(section)
        if not section_was_replaced:
            self.log.warning(
                f"Unable to replace section with name {new_section.section_name()} "
                f"because no RichChkSection was found with that section name"
            )
        return modified_sections

    @classmethod
    def add_chk_section(
        cls, new_section: Union[DecodedChkSection, RichChkSection], chk: RichChk
    ) -> RichChk:
        """Adds a new section to the CHK.

        Throws if the section already exists.
        """
        if chk.get_sections_by_name(new_section.section_name()):
            msg = (
                f"Cannot add CHK section with name {new_section.section_name()} "
                f"as it already exists in the CHK!"
            )
            raise ValueError(msg)
        new_sections = [section for section in chk.chk_sections]
        new_sections.append(new_section)
        return RichChk(_chk_sections=new_sections)

    @classmethod
    def remove_chk_sections_by_name(
        cls, section_to_remove: ChkSectionName, chk: RichChk
    ) -> RichChk:
        """Make a new CHK with all sections matching the name removed."""
        new_sections = [
            section
            for section in chk.chk_sections
            if section.section_name() != section_to_remove
        ]
        return RichChk(_chk_sections=new_sections)
