""""""

from chkjson.editor.richchk.rich_chk_editor import RichChkEditor
from chkjson.model.richchk.rich_chk import RichChk
from chkjson.model.richchk.unis.unit_id import UnitId
from chkjson.model.richchk.unix.rich_unix_section import RichUnixSection

from .fixtures.unit_settings_fixtures import (
    generate_rich_unix_with_terran_marine_setting,
    generate_unit_setting,
)


def test_it_replaces_rich_chk_section():
    rich_unix_with_terran_marine_setting = (
        generate_rich_unix_with_terran_marine_setting()
    )
    editor = RichChkEditor()
    rich_chk = RichChk(_chk_sections=[rich_unix_with_terran_marine_setting])
    new_unix = RichUnixSection(
        _unit_settings=[
            generate_unit_setting(UnitId.ZERG_ZERGLING),
            generate_unit_setting(UnitId.TERRAN_MARINE),
        ]
    )
    modified_rich_chk = editor.replace_chk_section(new_unix, rich_chk)
    assert new_unix in modified_rich_chk.chk_sections
    assert rich_unix_with_terran_marine_setting not in modified_rich_chk.chk_sections


def test_it_does_not_modify_rich_chk_if_section_not_found():
    editor = RichChkEditor()
    rich_chk = RichChk(_chk_sections=[])
    new_unix = RichUnixSection(
        _unit_settings=[
            generate_unit_setting(UnitId.ZERG_ZERGLING),
            generate_unit_setting(UnitId.TERRAN_MARINE),
        ]
    )
    modified_rich_chk = editor.replace_chk_section(new_unix, rich_chk)
    assert new_unix not in modified_rich_chk.chk_sections
    assert modified_rich_chk == rich_chk
