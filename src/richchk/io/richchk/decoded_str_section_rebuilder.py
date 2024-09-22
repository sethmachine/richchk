"""Rebuild a new DecodedStrSection from a RichChk."""

import dataclasses

from richchk.io.richchk.query.chk_query_util import ChkQueryUtil

from ...editor.chk.decoded_str_section_editor import DecodedStrSectionEditor
from ...model.chk.str.decoded_str_section import DecodedStrSection
from ...model.richchk.rich_chk import RichChk
from ...model.richchk.rich_chk_section import RichChkSection
from ...model.richchk.str.rich_string import RichNullString, RichString


class DecodedStrSectionRebuilder:
    @staticmethod
    def rebuild_str_section_from_rich_chk(rich_chk: RichChk) -> DecodedStrSection:
        decoded_str = ChkQueryUtil.find_only_decoded_section_in_chk(
            DecodedStrSection, rich_chk
        )
        rich_strings: set[
            RichString
        ] = DecodedStrSectionRebuilder.find_all_rich_strings_in_rich_chk(rich_chk)
        str_editor: DecodedStrSectionEditor = DecodedStrSectionEditor()
        return str_editor.add_strings_to_str_section(
            [x.value for x in rich_strings], decoded_str
        )

    @staticmethod
    def find_all_rich_strings_in_rich_chk(rich_chk: RichChk) -> set[RichString]:
        """Recursively search all RichCkSection for every unique RichString."""
        rich_sections = [
            section
            for section in rich_chk.chk_sections
            if isinstance(section, RichChkSection)
        ]
        return DecodedStrSectionRebuilder._walk_object_for_rich_strings(rich_sections)

    @staticmethod
    def _walk_object_for_rich_strings(obj: object) -> set[RichString]:
        strings = set()
        if isinstance(obj, RichString) and not isinstance(obj, RichNullString):
            strings.add(obj)
        elif isinstance(obj, (list, set, tuple)):
            for element in obj:
                strings = strings.union(
                    DecodedStrSectionRebuilder._walk_object_for_rich_strings(element)
                )
        elif isinstance(obj, dict):
            for key, value in obj.items():
                strings = strings.union(
                    DecodedStrSectionRebuilder._walk_object_for_rich_strings(key),
                    DecodedStrSectionRebuilder._walk_object_for_rich_strings(value),
                )
        elif dataclasses.is_dataclass(obj):
            for field in dataclasses.fields(obj):
                field_value = getattr(obj, field.name)
                strings = strings.union(
                    DecodedStrSectionRebuilder._walk_object_for_rich_strings(
                        field_value
                    )
                )
        return strings
