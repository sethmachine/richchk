"""Query DecodedChk and RichChk sections."""

from typing import Type, TypeVar, Union

from ...model.chk.decoded_chk import DecodedChk
from ...model.chk.decoded_chk_section import DecodedChkSection
from ...model.chk_section_name import ChkSectionName
from ...model.richchk.rich_chk import RichChk
from ...model.richchk.rich_chk_section import RichChkSection

_T = TypeVar("_T", bound=RichChkSection, covariant=True)
_U = TypeVar("_U", bound=DecodedChkSection, covariant=True)


class ChkQueryUtil:
    @staticmethod
    def find_only_decoded_section_in_chk(
        chk_section_type: Type[_U], chk: Union[DecodedChk, RichChk]
    ) -> _U:
        """Find the only DecodedChkSection with the given name.

        Throws if the section does not exist or there is more than 1 section with the
        same name.

        :param chk_section_type:
        :param chk:
        :return:
        """
        named_sections: list[Union[DecodedChkSection, RichChkSection]] = []
        if isinstance(chk, RichChk):
            named_sections = chk.get_sections_by_name(
                chk_section_name=chk_section_type.section_name()
            )
        elif isinstance(chk, DecodedChk):
            decoded_chk_sections = chk.get_sections_by_name(
                chk_section_name=chk_section_type.section_name()
            )
            named_sections += decoded_chk_sections
        if not named_sections:
            msg = (
                f"The CHK has no {chk_section_type.section_name().value} sections present! "
                "The CHK may not be valid.  Only pass in valid CHK data."
            )
            raise ValueError(msg)
        if len(named_sections) > 1:
            msg = (
                f"The CHK has more than 1 {chk_section_type.section_name().value} sections present"
                f" when only 1 is expected!"
            )
            raise ValueError(msg)
        only_section = named_sections[0]
        if isinstance(only_section, RichChkSection):
            raise ValueError(
                f"Expected a DecodedChkSection but found a RichChkSection "
                f"for section named {chk_section_type.section_name().value}"
            )
        assert isinstance(only_section, chk_section_type)
        return only_section

    @staticmethod
    def find_only_rich_section_in_chk(
        chk_section_type: Type[_T], rich_chk: RichChk
    ) -> _T:
        """Find the only RichChkSection with the given name.

        Throws if the section does not exist or there is more than 1 section with the
        same name.

        :param chk_section_type:
        :param rich_chk:
        :return:
        """
        named_sections = rich_chk.get_sections_by_name(
            chk_section_name=chk_section_type.section_name()
        )
        if not named_sections:
            msg = (
                f"The CHK has no {chk_section_type.section_name().value} sections present! "
                "The CHK is not valid.  Only pass in valid CHK data."
            )
            raise ValueError(msg)
        if len(named_sections) > 1:
            msg = (
                f"The CHK has more than 1 {chk_section_type.section_name().value} sections present"
                f" when only 1 is expected!"
            )
            raise ValueError(msg)
        only_section = named_sections[0]
        if isinstance(only_section, DecodedChkSection):
            raise ValueError(
                f"Expected a RichChkSection but found a DecodedChkSection "
                f"for section named {chk_section_type.section_name().value}"
            )
        assert isinstance(only_section, chk_section_type)
        return only_section

    @staticmethod
    def determine_if_rich_chk_contains_section(
        chk_section_name: ChkSectionName, rich_chk: RichChk
    ) -> bool:
        named_sections = rich_chk.get_sections_by_name(
            chk_section_name=chk_section_name
        )
        return len(named_sections) > 0

    @staticmethod
    def determine_if_chk_contains_section(
        chk_section_name: ChkSectionName, chk: DecodedChk
    ) -> bool:
        named_sections = chk.get_sections_by_name(chk_section_name=chk_section_name)
        return len(named_sections) > 0
