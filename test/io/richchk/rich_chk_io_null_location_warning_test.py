import logging

from richchk.io.richchk.richchk_io import RichChkIo
from richchk.model.richchk.mrgn.rich_location import RichLocation, _RichNullLocation
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


def test_it_warns_once_naming_the_action_when_a_trigger_has_a_null_location(caplog):
    trig = RichTrigSection(
        _triggers=[
            _trigger(_RichNullLocation()),
            _trigger(_RichNullLocation()),
            _trigger(RichLocation(1, 2, 3, 4, RichString(_value="a"), _index=1)),
        ]
    )
    with caplog.at_level(logging.WARNING):
        RichChkIo()._warn_if_triggers_have_null_locations(trig)
    warnings = [r for r in caplog.records if "location ID 0" in r.getMessage()]
    assert len(warnings) == 1
    assert "2 trigger(s)" in warnings[0].getMessage()
    assert "SetDoodadStateAction x2" in warnings[0].getMessage()


def test_it_does_not_warn_when_every_location_is_set(caplog):
    trig = RichTrigSection(
        _triggers=[_trigger(RichLocation(1, 2, 3, 4, RichString(_value="a"), _index=1))]
    )
    with caplog.at_level(logging.WARNING):
        RichChkIo()._warn_if_triggers_have_null_locations(trig)
    assert not [r for r in caplog.records if "location ID 0" in r.getMessage()]
