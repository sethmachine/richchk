"""Placeholder for utility functions operating on DecodedChk objects."""

from ...model.chk.decoded_chk import DecodedChk
from ...model.chk.decoded_chk_section import DecodedChkSection
from ...model.chk.str.decoded_str_section import DecodedStrSection
from ...model.chk_section_name import ChkSectionName


def find_only_decoded_str_section(chk: DecodedChk) -> DecodedStrSection:
    """Find the DecodedStrSection in a DecodedChk.

    Throws if there is not exactly 1.
    """
    str_sections = chk.get_sections_by_name(ChkSectionName.STR)
    if not str_sections:
        msg = (
            "The decoded CHK has no STR section present! "
            "The CHK is not valid.  Only pass in valid CHK data."
        )
        raise ValueError(msg)
    if len(str_sections) > 1:
        msg = (
            "The decoded CHK has more than 1 STR section present! "
            "The CHK may be valid but this case is not handled. "
            "Only pass in CHK data with a single STR section."
        )
        raise ValueError(msg)
    only_str: DecodedStrSection = DecodedChkSection.cast(
        str_sections[0], DecodedStrSection
    )
    return only_str
