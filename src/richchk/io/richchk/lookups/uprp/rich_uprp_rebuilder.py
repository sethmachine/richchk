"""Rebuild a new RichUprpSection from a RichChk."""

import dataclasses

from .....editor.richchk.rich_uprp_editor import RichUprpEditor
from .....model.richchk.rich_chk import RichChk
from .....model.richchk.rich_chk_section import RichChkSection
from .....model.richchk.uprp.rich_cuwp_slot import RichCuwpSlot
from .....model.richchk.uprp.rich_uprp_section import RichUprpSection
from ....richchk.query.chk_query_util import ChkQueryUtil


class RichUprpRebuilder:
    @classmethod
    def rebuild_rich_uprp_section_from_rich_chk(
        cls, rich_chk: RichChk
    ) -> RichUprpSection:
        rich_uprp = cls._find_or_create_new_rich_uprp(rich_chk)
        cuwps_to_add = RichUprpRebuilder.find_all_rich_cuwps(rich_chk)
        return RichUprpEditor().add_cuwp_slots(cuwps_to_add, rich_uprp)

    @classmethod
    def _find_or_create_new_rich_uprp(cls, rich_chk: RichChk) -> RichUprpSection:
        if ChkQueryUtil.determine_if_chk_contains_section(
            RichUprpSection.section_name(), rich_chk
        ):
            return ChkQueryUtil.find_only_rich_section_in_chk(RichUprpSection, rich_chk)
        return RichUprpSection(_cuwp_slots=[])

    @staticmethod
    def find_all_rich_cuwps(rich_chk: RichChk) -> set[RichCuwpSlot]:
        """"""
        rich_sections = [
            section
            for section in rich_chk.chk_sections
            if isinstance(section, RichChkSection)
            and not isinstance(section, RichUprpSection)
        ]
        return RichUprpRebuilder._walk_object_for_rich_cuwp_slots(rich_sections)

    @classmethod
    def _walk_object_for_rich_cuwp_slots(cls, obj: object) -> set[RichCuwpSlot]:
        locations = set()
        if isinstance(obj, RichCuwpSlot):
            locations.add(obj)
        elif isinstance(obj, (list, set, tuple)):
            for element in obj:
                locations = locations.union(
                    cls._walk_object_for_rich_cuwp_slots(element)
                )
        elif isinstance(obj, dict):
            for key, value in obj.items():
                locations = locations.union(
                    cls._walk_object_for_rich_cuwp_slots(key),
                    cls._walk_object_for_rich_cuwp_slots(value),
                )
        elif dataclasses.is_dataclass(obj):
            for field in dataclasses.fields(obj):
                field_value = getattr(obj, field.name)
                locations = locations.union(
                    cls._walk_object_for_rich_cuwp_slots(field_value)
                )
        return locations
