import pytest

from richchk.editor.richchk.rich_upgx_editor import RichUpgxEditor
from richchk.model.richchk.upgrades.upgrade_id import UpgradeId
from richchk.model.richchk.upgs.upgrade_cost_setting import UpgradeCostSetting
from richchk.model.richchk.upgx.rich_upgx_section import RichUpgxSection

_ALL_UPGRADES = list(UpgradeId)


def _make_default_setting(upgrade_id: UpgradeId) -> UpgradeCostSetting:
    return UpgradeCostSetting(
        _upgrade_id=upgrade_id,
        _uses_default_settings=True,
        _base_mineral_cost=100,
        _mineral_cost_factor=100,
        _base_gas_cost=0,
        _gas_cost_factor=0,
        _base_research_time=1800,
        _research_time_factor=0,
    )


def _make_upgx() -> RichUpgxSection:
    settings = {upgrade: _make_default_setting(upgrade) for upgrade in _ALL_UPGRADES}
    return RichUpgxSection(_upgrade_cost_settings=settings)


@pytest.fixture
def default_upgx() -> RichUpgxSection:
    return _make_upgx()


def test_it_sets_upgrade_cost_setting(default_upgx):
    editor = RichUpgxEditor()
    new_setting = UpgradeCostSetting(
        _upgrade_id=UpgradeId.TERRAN_INFANTRY_ARMOR,
        _uses_default_settings=False,
        _base_mineral_cost=200,
        _mineral_cost_factor=150,
        _base_gas_cost=50,
        _gas_cost_factor=25,
        _base_research_time=3600,
        _research_time_factor=0,
    )
    updated = editor.set_upgrade_cost_setting(new_setting, default_upgx)
    assert updated.upgrade_cost_settings[UpgradeId.TERRAN_INFANTRY_ARMOR] == new_setting


def test_it_sets_bw_upgrade_cost_setting(default_upgx):
    editor = RichUpgxEditor()
    new_setting = UpgradeCostSetting(
        _upgrade_id=UpgradeId.ARGUS_JEWEL,
        _uses_default_settings=False,
        _base_mineral_cost=150,
        _mineral_cost_factor=100,
        _base_gas_cost=150,
        _gas_cost_factor=100,
        _base_research_time=2400,
        _research_time_factor=0,
    )
    updated = editor.set_upgrade_cost_setting(new_setting, default_upgx)
    assert updated.upgrade_cost_settings[UpgradeId.ARGUS_JEWEL] == new_setting


def test_it_does_not_mutate_original(default_upgx):
    editor = RichUpgxEditor()
    new_setting = UpgradeCostSetting(
        _upgrade_id=UpgradeId.TERRAN_INFANTRY_ARMOR,
        _uses_default_settings=False,
        _base_mineral_cost=200,
        _mineral_cost_factor=150,
        _base_gas_cost=50,
        _gas_cost_factor=25,
        _base_research_time=3600,
        _research_time_factor=0,
    )
    editor.set_upgrade_cost_setting(new_setting, default_upgx)
    assert (
        default_upgx.upgrade_cost_settings[
            UpgradeId.TERRAN_INFANTRY_ARMOR
        ].base_mineral_cost
        == 100
    )


def test_it_preserves_other_upgrade_settings(default_upgx):
    editor = RichUpgxEditor()
    new_setting = UpgradeCostSetting(
        _upgrade_id=UpgradeId.TERRAN_INFANTRY_ARMOR,
        _uses_default_settings=False,
        _base_mineral_cost=999,
        _mineral_cost_factor=999,
        _base_gas_cost=999,
        _gas_cost_factor=999,
        _base_research_time=9999,
        _research_time_factor=999,
    )
    updated = editor.set_upgrade_cost_setting(new_setting, default_upgx)
    for upgrade in _ALL_UPGRADES:
        if upgrade == UpgradeId.TERRAN_INFANTRY_ARMOR:
            continue
        assert updated.upgrade_cost_settings[upgrade].base_mineral_cost == 100


def test_apply_upgrade_cost_settings_merges_partial_dict(default_upgx):
    editor = RichUpgxEditor()
    new_armor = UpgradeCostSetting(
        _upgrade_id=UpgradeId.TERRAN_INFANTRY_ARMOR,
        _uses_default_settings=False,
        _base_mineral_cost=200,
        _mineral_cost_factor=150,
        _base_gas_cost=0,
        _gas_cost_factor=0,
        _base_research_time=3600,
        _research_time_factor=0,
    )
    new_argus = UpgradeCostSetting(
        _upgrade_id=UpgradeId.ARGUS_JEWEL,
        _uses_default_settings=False,
        _base_mineral_cost=300,
        _mineral_cost_factor=200,
        _base_gas_cost=0,
        _gas_cost_factor=0,
        _base_research_time=3600,
        _research_time_factor=0,
    )
    updates = {
        UpgradeId.TERRAN_INFANTRY_ARMOR: new_armor,
        UpgradeId.ARGUS_JEWEL: new_argus,
    }
    updated = editor.apply_upgrade_cost_settings(updates, default_upgx)
    assert updated.upgrade_cost_settings[UpgradeId.TERRAN_INFANTRY_ARMOR] == new_armor
    assert updated.upgrade_cost_settings[UpgradeId.ARGUS_JEWEL] == new_argus
    assert (
        updated.upgrade_cost_settings[UpgradeId.ZERG_CARAPACE].base_mineral_cost == 100
    )


def test_apply_upgrade_cost_settings_does_not_mutate_original(default_upgx):
    editor = RichUpgxEditor()
    new_armor = UpgradeCostSetting(
        _upgrade_id=UpgradeId.TERRAN_INFANTRY_ARMOR,
        _uses_default_settings=False,
        _base_mineral_cost=200,
        _mineral_cost_factor=150,
        _base_gas_cost=0,
        _gas_cost_factor=0,
        _base_research_time=3600,
        _research_time_factor=0,
    )
    editor.apply_upgrade_cost_settings(
        {UpgradeId.TERRAN_INFANTRY_ARMOR: new_armor}, default_upgx
    )
    assert (
        default_upgx.upgrade_cost_settings[
            UpgradeId.TERRAN_INFANTRY_ARMOR
        ].base_mineral_cost
        == 100
    )
