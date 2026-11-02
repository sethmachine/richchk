from richchk.io.richchk.lookups.mrgn.rich_mrgn_section_rebuilder import (
    RichMrgnSectionRebuilder,
)
from richchk.model.richchk.mrgn.rich_location import RichLocation, _RichNullLocation
from richchk.model.richchk.mrgn.rich_mrgn_section import RichMrgnSection
from richchk.model.richchk.rich_chk import RichChk
from richchk.model.richchk.str.rich_string import RichString
from richchk.model.richchk.trig.actions.set_doodad_state_action import (
    SetDoodadStateAction,
)
from richchk.model.richchk.trig.enums.doodad_action import DoodadAction
from richchk.model.richchk.trig.player_id import PlayerId
from richchk.model.richchk.trig.rich_trig_section import RichTrigSection
from richchk.model.richchk.trig.rich_trigger import RichTrigger
from richchk.model.richchk.unis.unit_id import UnitId


def _trigger(location: RichLocation) -> RichTrigger:
    return RichTrigger(
        _conditions=[],
        _actions=[
            SetDoodadStateAction(
                _group=PlayerId.PLAYER_1,
                _unit=UnitId.TERRAN_MARINE,
                _location=location,
                _doodad_action=DoodadAction.SET,
            )
        ],
        _players={PlayerId.PLAYER_1},
    )


def test_it_does_not_add_null_or_unused_slot_locations_to_the_mrgn():
    used = RichLocation(1, 2, 3, 4, RichString(_value="used"), _index=5)
    mrgn = RichMrgnSection(_locations=[used])
    trig = RichTrigSection(
        _triggers=[
            _trigger(used),
            _trigger(_RichNullLocation()),
            _trigger(RichLocation.unused_slot(14)),
        ]
    )
    rich_chk = RichChk(_chk_sections=[mrgn, trig])
    new_mrgn, lookup = RichMrgnSectionRebuilder.rebuild_rich_mrgn_section_from_rich_chk(
        rich_chk
    )
    assert new_mrgn.locations == [used]
    assert lookup.get_id_by_location_or_throw(used) == 5
    assert lookup.get_id_by_location_or_throw(_RichNullLocation()) == 0
    assert lookup.get_id_by_location_or_throw(RichLocation.unused_slot(14)) == 14


def test_it_does_not_add_null_or_unused_slot_locations_when_rebuilding_from_locations():
    used = RichLocation(1, 2, 3, 4, RichString(_value="used"), _index=5)
    mrgn = RichMrgnSection(_locations=[used])
    rich_chk = RichChk(_chk_sections=[mrgn])
    new_mrgn, lookup = RichMrgnSectionRebuilder.rebuild_from_locations(
        {used, _RichNullLocation(), RichLocation.unused_slot(14)}, rich_chk
    )
    assert new_mrgn.locations == [used]
    assert lookup.get_id_by_location_or_throw(_RichNullLocation()) == 0
