"""Display a "Hello World!" message in a StarCraft map.

This also sets all unit names to "Hello World!" to demonstrate how to edit unit data.
"""

from decimal import Decimal

from richchk.editor.richchk.rich_chk_editor import RichChkEditor
from richchk.editor.richchk.rich_trig_editor import RichTrigEditor
from richchk.editor.richchk.rich_unix_editor import RichUnixEditor
from richchk.io.mpq.starcraft_mpq_io_helper import StarCraftMpqIoHelper
from richchk.io.richchk.query.chk_query_util import ChkQueryUtil
from richchk.model.richchk.str.rich_string import RichString
from richchk.model.richchk.trig.actions.display_text_message_action import (
    DisplayTextMessageAction,
)
from richchk.model.richchk.trig.conditions.always_condition import AlwaysCondition
from richchk.model.richchk.trig.player_id import PlayerId
from richchk.model.richchk.trig.rich_trig_section import RichTrigSection
from richchk.model.richchk.trig.rich_trigger import RichTrigger
from richchk.model.richchk.unis.unit_id import UnitId
from richchk.model.richchk.unis.unit_setting import UnitSetting
from richchk.model.richchk.unis.unit_to_weapon_lookup import get_weapons_for_unit
from richchk.model.richchk.unis.weapon_setting import WeaponSetting
from richchk.model.richchk.unix.rich_unix_section import RichUnixSection

# replace this with the path to the DLL on your local computer
PATH_TO_STORMLIB_DLL = None
INPUT_MAP_FILE = "maps/base-map.scx"
OUTPUT_MAP_FILE = "generated-maps/hello-world-generated.scx"

BLACKLISTED_UNIT_IDS = [
    UnitId.ANY_UNIT,
    UnitId.NO_UNIT,
    UnitId.MEN,
    UnitId.FACTORIES,
    UnitId.BUILDINGS,
]


def generate_unit_settings() -> list[UnitSetting]:
    settings = []
    for unit in UnitId:
        if unit in BLACKLISTED_UNIT_IDS:
            continue
        ws = [
            WeaponSetting(_weapon_id=weapon, _base_damage=1, _upgrade_damage=1)
            for weapon in get_weapons_for_unit(unit)
        ]
        # the default unit settings are not stored in the CHK
        # so we must fully replace each value even if we wish to only edit a single setting
        us = UnitSetting(
            _unit_id=unit,
            _hitpoints=Decimal(1),
            _shieldpoints=1,
            _armorpoints=1,
            _build_time=1,
            _mineral_cost=1,
            _gas_cost=1,
            _custom_unit_name=RichString(_value="Hello world!"),
            _weapons=ws,
        )
        settings.append(us)
    return settings


def generate_display_hello_world_trigger():
    return RichTrigger(
        _conditions=[AlwaysCondition()],
        _actions=[DisplayTextMessageAction(_text=RichString(_value="Hello world!"))],
        _players={PlayerId.ALL_PLAYERS},
    )


if __name__ == "__main__":
    mpqio = StarCraftMpqIoHelper.create_mpq_io(PATH_TO_STORMLIB_DLL)
    chk = mpqio.read_chk_from_mpq(INPUT_MAP_FILE)
    new_unit_settings = generate_unit_settings()
    new_unix = RichUnixEditor().upsert_all_unit_settings(
        new_unit_settings,
        ChkQueryUtil.find_only_rich_section_in_chk(RichUnixSection, chk),
    )
    new_trig = RichTrigEditor().add_triggers(
        [generate_display_hello_world_trigger()],
        ChkQueryUtil.find_only_rich_section_in_chk(RichTrigSection, chk),
    )
    new_chk = RichChkEditor().replace_chk_section(
        new_trig, RichChkEditor().replace_chk_section(new_unix, chk)
    )
    mpqio.save_chk_to_mpq(
        new_chk, INPUT_MAP_FILE, OUTPUT_MAP_FILE, overwrite_existing=True
    )
