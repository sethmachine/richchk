"""Add Hyper Triggers to a map.

This demonstrates how adding hyper triggers makes trigger cycles much faster, causing
units to spawn quicker.

This is based off the discussion here:
http://www.staredit.net/topic/16433/
"""

from richchk.editor.richchk.rich_chk_editor import RichChkEditor
from richchk.editor.richchk.rich_trig_editor import RichTrigEditor
from richchk.io.mpq.starcraft_mpq_io_helper import StarCraftMpqIoHelper
from richchk.io.richchk.query.chk_query_util import ChkQueryUtil
from richchk.io.richchk.query.mrgn_query_util import MrgnQueryUtil
from richchk.model.richchk.mrgn.rich_location import RichLocation
from richchk.model.richchk.mrgn.rich_mrgn_section import RichMrgnSection
from richchk.model.richchk.trig.actions.create_unit_action import CreateUnitAction
from richchk.model.richchk.trig.actions.preserve_trigger_action import PreserveTrigger
from richchk.model.richchk.trig.actions.set_deaths_action import SetDeathsAction
from richchk.model.richchk.trig.actions.wait_trigger_action import WaitAction
from richchk.model.richchk.trig.conditions.always_condition import AlwaysCondition
from richchk.model.richchk.trig.conditions.comparators.numeric_comparator import (
    NumericComparator,
)
from richchk.model.richchk.trig.conditions.deaths_condition import DeathsCondition
from richchk.model.richchk.trig.enums.amount_modifier import AmountModifier
from richchk.model.richchk.trig.player_id import PlayerId
from richchk.model.richchk.trig.rich_trig_section import RichTrigSection
from richchk.model.richchk.trig.rich_trigger import RichTrigger
from richchk.model.richchk.unis.unit_id import UnitId

# replace this with the path to the DLL on your local computer
PATH_TO_STORMLIB_DLL = None
INPUT_MAP_FILE = "maps/base-map.scx"
OUTPUT_MAP_FILE = "generated-maps/hyper-triggers-generated.scx"


def create_hyper_triggers():
    return RichTrigger(
        _conditions=[
            DeathsCondition(
                _group=PlayerId.ALL_PLAYERS,
                _comparator=NumericComparator.EXACTLY,
                _amount=0,
                _unit=UnitId.CAVE,
            )
        ],
        _actions=[
            SetDeathsAction(
                _group=PlayerId.CURRENT_PLAYER,
                _unit=UnitId.CAVE,
                _amount=1,
                _amount_modifier=AmountModifier.SET_TO,
            ),
            WaitAction(_milliseconds=0),
            SetDeathsAction(
                _group=PlayerId.CURRENT_PLAYER,
                _unit=UnitId.CAVE,
                _amount=0,
                _amount_modifier=AmountModifier.SET_TO,
            ),
            WaitAction(_milliseconds=0),
            PreserveTrigger(),
        ],
        _players={PlayerId.ALL_PLAYERS},
    )


def create_unit_spawn_trigger(spawn_location: RichLocation):
    return RichTrigger(
        _conditions=[AlwaysCondition()],
        _actions=[
            CreateUnitAction(
                _group=PlayerId.ALL_PLAYERS,
                _amount=1,
                _unit=UnitId.ZERG_ZERGLING,
                _location=spawn_location,
            ),
            PreserveTrigger(),
        ],
        _players={PlayerId.ALL_PLAYERS},
    )


if __name__ == "__main__":
    mpqio = StarCraftMpqIoHelper.create_mpq_io(PATH_TO_STORMLIB_DLL)
    chk = mpqio.read_chk_from_mpq(INPUT_MAP_FILE)
    anywhere_loc = MrgnQueryUtil.find_location_by_fuzzy_search(
        "anywhere", ChkQueryUtil.find_only_rich_section_in_chk(RichMrgnSection, chk)
    )
    new_trig = RichTrigEditor().add_triggers(
        [create_hyper_triggers(), create_unit_spawn_trigger(anywhere_loc)],
        ChkQueryUtil.find_only_rich_section_in_chk(RichTrigSection, chk),
    )
    new_chk = RichChkEditor().replace_chk_section(new_trig, chk)
    mpqio.save_chk_to_mpq(
        new_chk, INPUT_MAP_FILE, OUTPUT_MAP_FILE, overwrite_existing=True
    )
