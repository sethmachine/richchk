"""Rebuild a new RichSwnm from RichChk.

This rebuilds the SWNM, on top of making sure all switches are allocated a ID/index.
There is a maximum of 256 switches.
"""

import dataclasses
from typing import Tuple

from richchk.io.richchk.search.chk_query_util import ChkQueryUtil

from .....model.chk.swnm.swnm_constants import MAX_SWITCHES
from .....model.richchk.rich_chk import RichChk
from .....model.richchk.rich_chk_section import RichChkSection
from .....model.richchk.str.rich_string import RichNullString
from .....model.richchk.swnm.rich_switch import RichSwitch
from .....model.richchk.swnm.rich_swnm_lookup import RichSwnmLookup
from .....model.richchk.swnm.rich_swnm_section import RichSwnmSection
from .....util import logger


class RichSwnmRebuilder:
    _LOG = logger.get_logger("RichSwnmRebuilder")

    @classmethod
    def rebuild_rich_swnm_from_rich_chk(
        cls, rich_chk: RichChk
    ) -> Tuple[RichSwnmSection, RichSwnmLookup]:
        swnm = cls._find_or_create_rich_swnm(rich_chk)
        used_switches = cls._find_all_switches_in_rich_chk(rich_chk)
        switches_in_swnm_with_names = {
            x
            for x in swnm.switches
            if not cls._determine_if_switch_has_no_custom_name(x)
        }
        all_used_switches = used_switches.union(switches_in_swnm_with_names)
        allocable_ids = cls._generate_allocable_ids(all_used_switches)
        allocable_id_pointer = 0
        new_switches = [
            RichSwitch(_custom_name=RichNullString(), _index=switch_index)
            for switch_index in range(0, MAX_SWITCHES)
        ]
        id_by_switch = {}
        for used_switch in all_used_switches:
            if used_switch.index is not None:
                new_switches[used_switch.index] = used_switch
                id_by_switch[used_switch] = used_switch.index
            else:
                if allocable_id_pointer > len(allocable_ids) - 1:
                    msg = f"No more allocable switch IDs left.  Cannot use more than {MAX_SWITCHES} switches."
                    cls._LOG.error(msg)
                    raise ValueError(msg)
                else:
                    id_ = allocable_ids[allocable_id_pointer]
                    new_switches[id_] = RichSwitch(
                        _custom_name=used_switch.custom_name, _index=id_
                    )
                    id_by_switch[used_switch] = id_
                    allocable_id_pointer += 1
        return RichSwnmSection(_switches=new_switches), RichSwnmLookup(
            _switch_by_id_lookup={}, _id_by_switch_lookup=id_by_switch
        )

    @classmethod
    def _find_all_switches_in_rich_chk(cls, rich_chk: RichChk) -> set[RichSwitch]:
        """Recursively search all RichCkSection for every unique RichSwitch that is
        used.

        A switch is used if it has a custom name, or appears at least once in any
        trigger condition/action.  Skips SWNM section, from which is unioned all
        switches with custom names.
        """
        rich_sections = [
            section
            for section in rich_chk.chk_sections
            if isinstance(section, RichChkSection)
            and not isinstance(section, RichSwnmSection)
        ]
        return RichSwnmRebuilder._walk_object_for_rich_switch(rich_sections)

    @staticmethod
    def _walk_object_for_rich_switch(obj: object) -> set[RichSwitch]:
        switches = set()
        if isinstance(obj, RichSwitch):
            switches.add(obj)
        elif isinstance(obj, (list, set, tuple)):
            for element in obj:
                switches = switches.union(
                    RichSwnmRebuilder._walk_object_for_rich_switch(element)
                )
        elif isinstance(obj, dict):
            for key, value in obj.items():
                switches = switches.union(
                    RichSwnmRebuilder._walk_object_for_rich_switch(key),
                    RichSwnmRebuilder._walk_object_for_rich_switch(value),
                )
        elif dataclasses.is_dataclass(obj):
            for field in dataclasses.fields(obj):
                field_value = getattr(obj, field.name)
                switches = switches.union(
                    RichSwnmRebuilder._walk_object_for_rich_switch(field_value)
                )
        return switches

    @classmethod
    def _generate_allocable_ids(cls, switches: set[RichSwitch]) -> list[int]:
        """Generate all available ids when adding a new switch to the SWNM.

        :param switches: every used switch in the CHK. A used switch has a custom name
            and/or appears in at least 1 trigger action/condition.
        """
        possible_ids = range(0, MAX_SWITCHES)
        already_used_ids = [x.index for x in switches if x.index is not None]
        return [index for index in possible_ids if index not in already_used_ids]

    @classmethod
    def _determine_if_switch_has_no_custom_name(cls, switch: RichSwitch) -> bool:
        if switch.custom_name:
            return isinstance(switch.custom_name, RichNullString) or (
                not switch.custom_name.value
            )
        return True

    @classmethod
    def _find_or_create_rich_swnm(cls, rich_chk: RichChk) -> RichSwnmSection:
        try:
            swnm = ChkQueryUtil.find_only_rich_section_in_chk(RichSwnmSection, rich_chk)
            return swnm
        except ValueError:
            cls._LOG.info("No RichSwnm found; creating a new SWNM section")
            return cls._generate_empty_swnm()

    @classmethod
    def _generate_empty_swnm(cls) -> RichSwnmSection:
        return RichSwnmSection(
            _switches=[RichSwitch(_index=index) for index in range(0, MAX_SWITCHES)]
        )
