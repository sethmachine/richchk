import pytest

from richchk.io.richchk.lookups.swnm.rich_swnm_rebuilder import RichSwnmRebuilder
from richchk.model.chk.swnm.swnm_constants import MAX_SWITCHES
from richchk.model.richchk.rich_chk import RichChk
from richchk.model.richchk.str.rich_string import RichNullString, RichString
from richchk.model.richchk.swnm.rich_switch import RichSwitch
from richchk.model.richchk.swnm.rich_swnm_section import RichSwnmSection
from richchk.model.richchk.trig.conditions.switch_condition import SwitchCondition
from richchk.model.richchk.trig.enums.switch_state import SwitchState
from richchk.model.richchk.trig.rich_trig_section import RichTrigSection
from richchk.model.richchk.trig.rich_trigger import RichTrigger


@pytest.fixture(scope="function")
def rich_chk_with_switches() -> RichChk:
    return RichChk(
        _chk_sections=[
            RichSwnmSection(
                _switches=[
                    RichSwitch(RichNullString(), _index=x)
                    for x in range(0, MAX_SWITCHES)
                ]
            ),
            RichTrigSection(
                _triggers=[
                    RichTrigger(
                        _conditions=[
                            SwitchCondition(
                                _switch_state=SwitchState.CLEARED,
                                _switch=RichSwitch(
                                    _custom_name=RichString(_value="hello world"),
                                    _index=0,
                                ),
                            ),
                            SwitchCondition(
                                _switch_state=SwitchState.SET,
                                _switch=RichSwitch(
                                    _custom_name=RichString(
                                        _value="switch without index"
                                    ),
                                    _index=None,
                                ),
                            ),
                            SwitchCondition(
                                _switch_state=SwitchState.SET,
                                _switch=RichSwitch(
                                    _custom_name=RichString(
                                        _value="switch without index"
                                    ),
                                    _index=None,
                                ),
                            ),
                            SwitchCondition(
                                _switch_state=SwitchState.SET,
                                _switch=RichSwitch(
                                    _custom_name=RichNullString(),
                                    _index=200,
                                ),
                            ),
                            SwitchCondition(
                                _switch_state=SwitchState.SET,
                                _switch=RichSwitch(
                                    _custom_name=RichNullString(),
                                    _index=200,
                                ),
                            ),
                        ],
                        _actions=[],
                        _players=set(),
                    )
                ]
            ),
        ]
    )


@pytest.fixture(scope="function")
def rich_chk_with_more_than_max_unique_switches() -> RichChk:
    return RichChk(
        _chk_sections=[
            RichSwnmSection(
                _switches=[
                    RichSwitch(RichNullString(), _index=x)
                    for x in range(0, MAX_SWITCHES)
                ]
            ),
            RichTrigSection(
                _triggers=[
                    RichTrigger(
                        _conditions=[
                            SwitchCondition(
                                _switch_state=SwitchState.SET, _switch=RichSwitch()
                            )
                            for _ in range(0, MAX_SWITCHES + 100)
                        ],
                        _actions=[],
                        _players=set(),
                    )
                ]
            ),
        ]
    )


@pytest.fixture(scope="function")
def rich_chk_with_more_than_max_switches_but_not_all_unique() -> RichChk:
    return RichChk(
        _chk_sections=[
            RichSwnmSection(
                _switches=[
                    RichSwitch(RichNullString(), _index=x)
                    for x in range(0, MAX_SWITCHES)
                ]
            ),
            RichTrigSection(
                _triggers=[
                    RichTrigger(
                        _conditions=[
                            SwitchCondition(
                                _switch_state=SwitchState.SET,
                                _switch=RichSwitch(_index=100),
                            )
                            for _ in range(0, MAX_SWITCHES + 100)
                        ]
                        + [
                            SwitchCondition(
                                _switch_state=SwitchState.SET,
                                _switch=RichSwitch(
                                    _custom_name=RichString(
                                        "unique switch used many times"
                                    )
                                ),
                            )
                            for _ in range(0, MAX_SWITCHES + 100)
                        ],
                        _actions=[],
                        _players=set(),
                    )
                ]
            ),
        ]
    )


def test_it_rebuilds_rich_swnm(rich_chk_with_switches):
    new_swnm, _ = RichSwnmRebuilder.rebuild_rich_swnm_from_rich_chk(
        rich_chk_with_switches
    )
    assert all([s.index is not None for s in new_swnm.switches])
    assert new_swnm.switches[0] == RichSwitch(
        _custom_name=RichString(_value="hello world"),
        _index=0,
    )
    assert any(
        [
            s.custom_name == RichString(_value="switch without index")
            for s in new_swnm.switches
        ]
    )


def test_it_throws_if_more_than_max_unique_switches_allocated(
    rich_chk_with_more_than_max_unique_switches,
):
    with pytest.raises(ValueError):
        RichSwnmRebuilder.rebuild_rich_swnm_from_rich_chk(
            rich_chk_with_more_than_max_unique_switches
        )


def test_it_allocates_more_than_max_switches_if_not_all_unique(
    rich_chk_with_more_than_max_switches_but_not_all_unique,
):
    new_swnm, _ = RichSwnmRebuilder.rebuild_rich_swnm_from_rich_chk(
        rich_chk_with_more_than_max_switches_but_not_all_unique
    )
    assert all([s.index is not None for s in new_swnm.switches])
    unique_switch = [
        s
        for s in new_swnm.switches
        if s.custom_name == RichString(_value="unique switch used many times")
    ]
    assert len(unique_switch) == 1
