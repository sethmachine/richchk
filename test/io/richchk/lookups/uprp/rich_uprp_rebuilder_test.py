from test.fixtures.cuwp_fixtures import generate_cuwp_slot
from test.fixtures.location_fixtures import generate_rich_location

import pytest

from richchk.io.richchk.lookups.uprp.rich_uprp_rebuilder import RichUprpRebuilder
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
from richchk.model.richchk.uprp.rich_uprp_section import RichUprpSection
from richchk.util.dataclasses_util import build_dataclass_with_fields


@pytest.fixture(scope="function")
def rich_chk_with_new_cuwps() -> tuple[RichChk, list[RichCuwpSlot]]:
    expected_cuwps = [
        generate_cuwp_slot(index=1),
        build_dataclass_with_fields(generate_cuwp_slot(), _hallucinated=True),
        build_dataclass_with_fields(generate_cuwp_slot(), _burrowed=True),
    ]
    return (
        RichChk(
            _chk_sections=[
                RichUprpSection(_cuwp_slots=[generate_cuwp_slot(index=1)]),
                RichTrigSection(
                    _triggers=[
                        RichTrigger(
                            _conditions=[AlwaysCondition()],
                            _actions=[
                                CreateUnitWithPropertiesAction(
                                    _group=PlayerId.PLAYER_1,
                                    _amount=1,
                                    _unit=UnitId.TERRAN_MARINE,
                                    _location=generate_rich_location(),
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
                                    _location=generate_rich_location(),
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


def test_it_rebuilds_rich_uprp(rich_chk_with_new_cuwps):
    rich_chk, expected_cuwps = rich_chk_with_new_cuwps
    new_uprp = RichUprpRebuilder.rebuild_rich_uprp_section_from_rich_chk(rich_chk)
    assert all([x.index is not None for x in new_uprp.cuwp_slots])
    assert len(new_uprp.cuwp_slots) == 3
    for cuwp in expected_cuwps:
        assert cuwp in new_uprp.cuwp_slots


def test_it_creates_a_new_uprp_if_none_existed_before(rich_chk_with_new_cuwps):
    rich_chk, expected_cuwps = rich_chk_with_new_cuwps
    chk_without_uprp = RichChk(
        _chk_sections=[
            x for x in rich_chk.chk_sections if not isinstance(x, RichUprpSection)
        ]
    )
    new_uprp = RichUprpRebuilder.rebuild_rich_uprp_section_from_rich_chk(
        chk_without_uprp
    )
    assert len(new_uprp.cuwp_slots) == 2
    # skip the first 1, since it's only in the UPRP
    for cuwp in expected_cuwps[1:]:
        assert cuwp in new_uprp.cuwp_slots
