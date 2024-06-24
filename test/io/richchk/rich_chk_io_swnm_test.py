import pytest

from richchk.io.richchk.richchk_io import RichChkIo
from richchk.io.util.chk_query_util import ChkQueryUtil
from richchk.model.chk.str.decoded_str_section import DecodedStrSection
from richchk.model.chk_section_name import ChkSectionName
from richchk.model.richchk.mrgn.rich_mrgn_section import RichMrgnSection
from richchk.model.richchk.rich_chk import RichChk
from richchk.model.richchk.str.rich_string import RichString
from richchk.model.richchk.swnm.rich_switch import RichSwitch
from richchk.model.richchk.swnm.rich_swnm_section import RichSwnmSection
from richchk.model.richchk.trig.actions.set_switch_action import SetSwitchAction
from richchk.model.richchk.trig.conditions.switch_condition import SwitchCondition
from richchk.model.richchk.trig.enums.switch_action import SwitchAction
from richchk.model.richchk.trig.enums.switch_state import SwitchState
from richchk.model.richchk.trig.rich_trig_section import RichTrigSection
from richchk.model.richchk.trig.rich_trigger import RichTrigger


@pytest.fixture(scope="function")
def rich_chk_with_no_switches():
    return RichChk(
        _chk_sections=[
            DecodedStrSection(
                # the first offset points to where the last offset ends in bytes
                # first 2 bytes are number of strings, next 2 bytes is the offset
                # so "a" starts at byte position 4 (0 indexed)
                _number_of_strings=1,
                _string_offsets=[4],
                _strings=["a"],
            ),
            RichMrgnSection(_locations=[]),
        ]
    )


@pytest.fixture(scope="function")
def rich_chk_with_switches():
    return RichChk(
        _chk_sections=[
            DecodedStrSection(
                # the first offset points to where the last offset ends in bytes
                # first 2 bytes are number of strings, next 2 bytes is the offset
                # so "a" starts at byte position 4 (0 indexed)
                _number_of_strings=1,
                _string_offsets=[4],
                _strings=["a"],
            ),
            RichMrgnSection(_locations=[]),
            RichSwnmSection(
                _switches=[RichSwitch(_custom_name=RichString(_value="a"), _index=7)]
                + ([RichSwitch()] * 255)
            ),
        ]
    )


def test_integration_it_adds_new_switches_when_they_are_used(rich_chk_with_no_switches):
    new_switch_with_name = RichSwitch(RichString("new switch"))
    new_switch_without_name = RichSwitch()
    triggers = RichTrigSection(
        _triggers=[
            RichTrigger(
                _conditions=[
                    SwitchCondition(
                        _switch_state=SwitchState.SET, _switch=new_switch_with_name
                    ),
                    SwitchCondition(
                        _switch_state=SwitchState.SET, _switch=new_switch_without_name
                    ),
                ],
                _actions=[
                    SetSwitchAction(
                        _switch=new_switch_with_name,
                        _switch_action=SwitchAction.RANDOMIZE,
                    )
                ],
                _players=set(),
            )
        ]
    )
    chk = RichChkIo().encode_chk(
        RichChk(_chk_sections=(rich_chk_with_no_switches.chk_sections + [triggers]))
    )
    assert ChkQueryUtil.determine_if_chk_contains_section(ChkSectionName.SWNM, chk)
    rich_chk_again = RichChkIo().decode_chk(chk)
    ChkQueryUtil.determine_if_rich_chk_contains_section(
        ChkSectionName.SWNM, rich_chk_again
    )
    swnm = ChkQueryUtil.find_only_rich_section_in_chk(RichSwnmSection, rich_chk_again)
    trig = ChkQueryUtil.find_only_rich_section_in_chk(RichTrigSection, rich_chk_again)
    assert_triggers_all_have_allocated_switches(trig.triggers)
    assert_switch_exists_with_rich_string(
        swnm.switches, new_switch_with_name.custom_name
    )


def test_integration_it_adds_new_switches_when_some_switches_already_exist(
    rich_chk_with_switches,
):
    new_switch_with_name = RichSwitch(RichString("new switch"))
    new_switch_without_name = RichSwitch()
    triggers = RichTrigSection(
        _triggers=[
            RichTrigger(
                _conditions=[
                    SwitchCondition(
                        _switch_state=SwitchState.SET, _switch=new_switch_with_name
                    ),
                    SwitchCondition(
                        _switch_state=SwitchState.SET, _switch=new_switch_without_name
                    ),
                ],
                _actions=[
                    SetSwitchAction(
                        _switch=new_switch_with_name,
                        _switch_action=SwitchAction.RANDOMIZE,
                    )
                ],
                _players=set(),
            )
        ]
    )
    chk = RichChkIo().encode_chk(
        RichChk(_chk_sections=(rich_chk_with_switches.chk_sections + [triggers]))
    )
    assert ChkQueryUtil.determine_if_chk_contains_section(ChkSectionName.SWNM, chk)
    rich_chk_again = RichChkIo().decode_chk(chk)
    ChkQueryUtil.determine_if_rich_chk_contains_section(
        ChkSectionName.SWNM, rich_chk_again
    )
    swnm = ChkQueryUtil.find_only_rich_section_in_chk(RichSwnmSection, rich_chk_again)
    trig = ChkQueryUtil.find_only_rich_section_in_chk(RichTrigSection, rich_chk_again)
    assert_triggers_all_have_allocated_switches(trig.triggers)
    assert_switch_exists_with_rich_string(
        swnm.switches, new_switch_with_name.custom_name
    )


def assert_switch_exists_with_rich_string(switches, rich_string):
    for switch in switches:
        if switch.custom_name == rich_string:
            return True
    return False


def assert_triggers_all_have_allocated_switches(triggers):
    for trig in triggers:
        for condition in trig.conditions:
            if isinstance(condition, SwitchCondition):
                assert condition.switch.index is not None
        for action in trig.actions:
            if isinstance(action, SetSwitchAction):
                assert action.switch.index is not None
