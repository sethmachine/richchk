"""Rebuild a new DecodedStrSection from a RichChk."""

import dataclasses
from collections import OrderedDict

from ...editor.chk.decoded_str_section_editor import DecodedStrSectionEditor
from ...model.chk.str.decoded_str_section import DecodedStrSection
from ...model.richchk.rich_chk import RichChk
from ...model.richchk.rich_chk_section import RichChkSection
from ...model.richchk.str.rich_string import RichNullString, RichString
from .query.chk_query_util import ChkQueryUtil


class DecodedStrSectionRebuilder:
    @staticmethod
    def rebuild_str_section_from_rich_chk(rich_chk: RichChk) -> DecodedStrSection:
        decoded_str = ChkQueryUtil.find_only_decoded_section_in_chk(
            DecodedStrSection, rich_chk
        )
        rich_strings: list[
            RichString
        ] = DecodedStrSectionRebuilder.find_all_rich_strings_in_rich_chk(rich_chk)
        str_editor: DecodedStrSectionEditor = DecodedStrSectionEditor()
        return str_editor.add_strings_to_str_section(
            [x.value for x in rich_strings], decoded_str
        )

    @staticmethod
    def find_all_rich_strings_in_rich_chk(rich_chk: RichChk) -> list[RichString]:
        """Recursively search all RichCkSection for every unique RichString."""
        rich_sections = [
            section
            for section in rich_chk.chk_sections
            if isinstance(section, RichChkSection)
        ]
        return list(
            DecodedStrSectionRebuilder._walk_object_for_rich_strings(
                rich_sections
            ).keys()
        )

    @staticmethod
    def _walk_object_for_rich_strings(obj: object) -> OrderedDict[RichString, int]:
        strings = OrderedDict()
        if isinstance(obj, RichString) and not isinstance(obj, RichNullString):
            strings[obj] = 0
        elif isinstance(obj, (list, set, tuple)):
            for element in obj:
                for key in DecodedStrSectionRebuilder._walk_object_for_rich_strings(
                    element
                ):
                    strings[key] = 0
        elif isinstance(obj, dict):
            for key, value in obj.items():
                for x in DecodedStrSectionRebuilder._walk_object_for_rich_strings(key):
                    strings[x] = 0
                for y in DecodedStrSectionRebuilder._walk_object_for_rich_strings(
                    value
                ):
                    strings[y] = 0
        elif dataclasses.is_dataclass(obj):
            for field in dataclasses.fields(obj):
                field_value = getattr(obj, field.name)
                for key in DecodedStrSectionRebuilder._walk_object_for_rich_strings(
                    field_value
                ):
                    strings[key] = 0
        return strings
