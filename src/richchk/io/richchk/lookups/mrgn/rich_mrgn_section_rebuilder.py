"""Rebuild a new RichMrgnSection from a RichChk.

This class scans for all RichLocation references among all RichChk sections that may not
alreadu exist in the MRGN, and adds them to the Rich MRGN.

Each RichLocation without an index is also assigned an index from any of the unused
location data slot.  There can be at most 255 locations, but 1 location is always
allocated to "Anywhere".
"""

import dataclasses

from .....editor.richchk.rich_mrgn_editor import RichMrgnEditor
from .....model.chk_section_name import ChkSectionName
from .....model.richchk.mrgn.rich_location import RichLocation
from .....model.richchk.mrgn.rich_mrgn_section import RichMrgnSection
from .....model.richchk.rich_chk import RichChk
from .....model.richchk.rich_chk_section import RichChkSection
from ....util.chk_query_util import ChkQueryUtil


class RichMrgnSectionRebuilder:
    @staticmethod
    def rebuild_rich_mrgn_section_from_rich_chk(rich_chk: RichChk) -> RichMrgnSection:
        rich_mrgn: RichMrgnSection = RichChkSection.cast(
            ChkQueryUtil.find_only_rich_section_in_chk(ChkSectionName.MRGN, rich_chk),
            RichMrgnSection,
        )
        all_rich_locations: set[
            RichLocation
        ] = RichMrgnSectionRebuilder.find_all_rich_locations_in_rich_chk(rich_chk)
        editor = RichMrgnEditor()
        return editor.add_locations(all_rich_locations, rich_mrgn)

    @staticmethod
    def find_all_rich_locations_in_rich_chk(rich_chk: RichChk) -> set[RichLocation]:
        """Recursively search all RichCkSection for every unique RichLocation.

        Skip searching any MRGN sections.
        """
        rich_sections = [
            section
            for section in rich_chk.chk_sections
            if isinstance(section, RichChkSection)
            and not isinstance(section, RichMrgnSection)
        ]
        return RichMrgnSectionRebuilder._walk_object_for_rich_locations(rich_sections)

    @staticmethod
    def _walk_object_for_rich_locations(obj: object) -> set[RichLocation]:
        locations = set()
        if isinstance(obj, RichLocation):
            locations.add(obj)
        elif isinstance(obj, (list, set, tuple)):
            for element in obj:
                locations = locations.union(
                    RichMrgnSectionRebuilder._walk_object_for_rich_locations(element)
                )
        elif isinstance(obj, dict):
            for key, value in obj.items():
                locations = locations.union(
                    RichMrgnSectionRebuilder._walk_object_for_rich_locations(key),
                    RichMrgnSectionRebuilder._walk_object_for_rich_locations(value),
                )
        elif dataclasses.is_dataclass(obj):
            for field in dataclasses.fields(obj):
                field_value = getattr(obj, field.name)
                locations = locations.union(
                    RichMrgnSectionRebuilder._walk_object_for_rich_locations(
                        field_value
                    )
                )
        return locations
