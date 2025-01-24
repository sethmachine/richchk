"""Replace or add existing DecodedChkSections to a DecodedChk."""

from ...model.chk.decoded_chk import DecodedChk
from ...model.chk.decoded_chk_section import DecodedChkSection
from ...model.chk_section_name import ChkSectionName
from ...util import logger


class DecodedChkEditor:

    _LOG = logger.get_logger("DecodedChkEditor")

    @classmethod
    def add_chk_section(
        cls, new_section: DecodedChkSection, chk: DecodedChk
    ) -> DecodedChk:
        """Adds a new section to the CHK.

        Throws if the section already exists.
        """
        if chk.get_sections_by_name(new_section.section_name()):
            msg = (
                f"Cannot add CHK section with name {new_section.section_name()} "
                f"as it already exists in the CHK!"
            )
            cls._LOG.error(msg)
            raise ValueError(msg)
        new_sections = [section for section in chk.decoded_chk_sections]
        new_sections.append(new_section)
        return DecodedChk(_decoded_chk_sections=new_sections)

    @classmethod
    def remove_chk_sections_by_name(
        cls, section_to_remove: ChkSectionName, chk: DecodedChk
    ) -> DecodedChk:
        """Make a new CHK with all sections matching the name removed."""
        new_sections = [
            section
            for section in chk.decoded_chk_sections
            if section.section_name() != section_to_remove
        ]
        return DecodedChk(_decoded_chk_sections=new_sections)
