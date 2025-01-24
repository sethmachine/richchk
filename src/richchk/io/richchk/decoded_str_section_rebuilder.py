"""Rebuild a new DecodedStrSection from a RichChk."""

import dataclasses
from collections import OrderedDict

from ...editor.chk.decoded_str_section_editor import DecodedStrSectionEditor
from ...editor.chk.decoded_strx_section_editor import DecodedStrxSectionEditor
from ...model.chk.decoded_string_section import DecodedStringSection
from ...model.chk.str.decoded_str_section import DecodedStrSection
from ...model.chk.strx.decoded_strx_section import DecodedStrxSection
from ...model.richchk.rich_chk import RichChk
from ...model.richchk.rich_chk_section import RichChkSection
from ...model.richchk.str.rich_string import RichNullString, RichString
from .query.chk_query_util import ChkQueryUtil


class DecodedStrSectionRebuilder:
    @staticmethod
    def rebuild_str_section_from_rich_chk(rich_chk: RichChk) -> DecodedStringSection:
        decoded_str = ChkQueryUtil.find_string_section_in_chk(rich_chk)
        rich_strings = DecodedStrSectionRebuilder.find_all_rich_strings_in_rich_chk(
            rich_chk
        )
        return DecodedStrSectionRebuilder._add_strings_to_string_section(
            [x.value for x in rich_strings], decoded_str
        )

    @staticmethod
    def _add_strings_to_string_section(
        strings_to_add: list[str], decoded_string_section: DecodedStringSection
    ) -> DecodedStringSection:
        if isinstance(decoded_string_section, DecodedStrSection):
            return DecodedStrSectionEditor().add_strings_to_str_section(
                strings_to_add, decoded_string_section
            )
        elif isinstance(decoded_string_section, DecodedStrxSection):
            return DecodedStrxSectionEditor().add_strings_to_strx_section(
                strings_to_add, decoded_string_section
            )
        raise ValueError("Unknown string section, got neither STR or STRx")

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
