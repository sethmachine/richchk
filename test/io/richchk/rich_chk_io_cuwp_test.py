"""Verify UPRP/CUWP are updated when create a new CHK."""
from test.fixtures.chk.str_fixtures import generate_decoded_str_section
from test.fixtures.cuwp_fixtures import generate_cuwp_slot
from test.fixtures.location_fixtures import generate_rich_location

import pytest

from richchk.io.richchk.richchk_io import RichChkIo
from richchk.io.util.chk_query_util import ChkQueryUtil
from richchk.model.chk_section_name import ChkSectionName
from richchk.model.richchk.mrgn.rich_mrgn_section import RichMrgnSection
from richchk.model.richchk.rich_chk import RichChk
from richchk.model.richchk.trig.actions.create_unit_with_properties_action import (
    CreateUnitWithPropertiesAction,
)
from richchk.model.richchk.trig.conditions.always_condition import AlwaysCondition
from richchk.model.richchk.trig.conditions.never_condition import NeverCondition
from richchk.model.richchk.trig.player_id import PlayerId
from richchk.model.richchk.trig.rich_trig_section import RichTrigSection
from richchk.model.richchk.trig.rich_trigger import RichTrigger
from richchk.model.richchk.unis.unit_id import UnitId
from richchk.model.richchk.uprp.rich_cuwp_slot import RichCuwpSlot
from richchk.util.dataclasses_util import build_dataclass_with_fields


@pytest.fixture(scope="function")
def rich_chk_with_new_cuwps() -> tuple[RichChk, list[RichCuwpSlot]]:
    location = generate_rich_location(index=1)
    expected_cuwps = [
        build_dataclass_with_fields(generate_cuwp_slot(), _hallucinated=True),
        build_dataclass_with_fields(generate_cuwp_slot(), _burrowed=True),
    ]
    return (
        RichChk(
            _chk_sections=[
                generate_decoded_str_section(),
                RichMrgnSection(_locations=[location]),
                RichTrigSection(
                    _triggers=[
                        RichTrigger(
                            _conditions=[AlwaysCondition()],
                            _actions=[
                                CreateUnitWithPropertiesAction(
                                    _group=PlayerId.PLAYER_1,
                                    _amount=1,
                                    _unit=UnitId.TERRAN_MARINE,
                                    _location=location,
                                    _properties=build_dataclass_with_fields(
                                        generate_cuwp_slot(), _hallucinated=True
                                    ),
                                )
                            ],
                            _players=set(),
                        ),
                        RichTrigger(
                            _conditions=[NeverCondition()],
                            _actions=[
                                CreateUnitWithPropertiesAction(
                                    _group=PlayerId.PLAYER_5,
                                    _amount=133,
                                    _unit=UnitId.ZERG_ZERGLING,
                                    _location=location,
                                    _properties=build_dataclass_with_fields(
                                        generate_cuwp_slot(), _burrowed=True
                                    ),
                                )
                            ],
                            _players=set(),
                        ),
                    ]
                ),
            ]
        ),
        expected_cuwps,
    )


def test_integration_it_creates_uprp_and_upus_if_they_did_not_exist_before(
    rich_chk_with_new_cuwps,
):
    rich_chk, expected_cuwps = rich_chk_with_new_cuwps
    chk = RichChkIo().encode_chk(rich_chk)
    assert ChkQueryUtil.determine_if_chk_contains_section(ChkSectionName.UPRP, chk)
    assert ChkQueryUtil.determine_if_chk_contains_section(ChkSectionName.UPUS, chk)
    rich_chk_again = RichChkIo().decode_chk(chk)
    ChkQueryUtil.determine_if_rich_chk_contains_section(
        ChkSectionName.UPRP, rich_chk_again
    )
    ChkQueryUtil.determine_if_rich_chk_contains_section(
        ChkSectionName.UPUS, rich_chk_again
    )
    trig = ChkQueryUtil.find_only_rich_section_in_chk(RichTrigSection, rich_chk_again)
    assert_triggers_all_have_allocated_cuwps(trig.triggers)
    # assert_switch_exists_with_rich_string(
    #     swnm.switches, new_switch_with_name.custom_name
    # )


# def test_integration_it_adds_new_switches_when_some_switches_already_exist(
#     rich_chk_with_switches,
# ):
#     new_switch_with_name = RichSwitch(RichString("new switch"))
#     new_switch_without_name = RichSwitch()
#     triggers = RichTrigSection(
#         _triggers=[
#             RichTrigger(
#                 _conditions=[
#                     SwitchCondition(
#                         _switch_state=SwitchState.SET, _switch=new_switch_with_name
#                     ),
#                     SwitchCondition(
#                         _switch_state=SwitchState.SET, _switch=new_switch_without_name
#                     ),
#                 ],
#                 _actions=[
#                     SetSwitchAction(
#                         _switch=new_switch_with_name,
#                         _switch_action=SwitchAction.RANDOMIZE,
#                     )
#                 ],
#                 _players=set(),
#             )
#         ]
#     )
#     chk = RichChkIo().encode_chk(
#         RichChk(_chk_sections=(rich_chk_with_switches.chk_sections + [triggers]))
#     )
#     assert ChkQueryUtil.determine_if_chk_contains_section(ChkSectionName.SWNM, chk)
#     rich_chk_again = RichChkIo().decode_chk(chk)
#     ChkQueryUtil.determine_if_rich_chk_contains_section(
#         ChkSectionName.SWNM, rich_chk_again
#     )
#     swnm = ChkQueryUtil.find_only_rich_section_in_chk(RichSwnmSection, rich_chk_again)
#     trig = ChkQueryUtil.find_only_rich_section_in_chk(RichTrigSection, rich_chk_again)
#     assert_triggers_all_have_allocated_switches(trig.triggers)
#     assert_switch_exists_with_rich_string(
#         swnm.switches, new_switch_with_name.custom_name
#     )
#
#
# def assert_switch_exists_with_rich_string(switches, rich_string):
#     for switch in switches:
#         if switch.custom_name == rich_string:
#             return True
#     return False
#
#
def assert_triggers_all_have_allocated_cuwps(triggers):
    for trig in triggers:
        for action in trig.actions:
            if isinstance(action, CreateUnitWithPropertiesAction):
                assert action.properties.index is not None
