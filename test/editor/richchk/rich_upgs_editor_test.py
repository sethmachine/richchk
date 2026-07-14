import pytest

from richchk.editor.richchk.rich_upgs_editor import RichUpgsEditor
from richchk.model.richchk.upgrades.upgrade_id import UpgradeId
from richchk.model.richchk.upgs.rich_upgs_section import RichUpgsSection
from richchk.model.richchk.upgs.upgrade_cost_setting import UpgradeCostSetting

_CLASSIC_UPGRADES = [u for u in UpgradeId if u.id < 46]


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


def _make_upgs() -> RichUpgsSection:
    settings = {
        upgrade: _make_default_setting(upgrade) for upgrade in _CLASSIC_UPGRADES
    }
    return RichUpgsSection(_upgrade_cost_settings=settings)


@pytest.fixture
def default_upgs() -> RichUpgsSection:
    return _make_upgs()


def test_it_sets_upgrade_cost_setting(default_upgs):
    editor = RichUpgsEditor()
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
    updated = editor.set_upgrade_cost_setting(new_setting, default_upgs)
    assert updated.upgrade_cost_settings[UpgradeId.TERRAN_INFANTRY_ARMOR] == new_setting


def test_it_does_not_mutate_original(default_upgs):
    editor = RichUpgsEditor()
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
    editor.set_upgrade_cost_setting(new_setting, default_upgs)
    assert (
        default_upgs.upgrade_cost_settings[
            UpgradeId.TERRAN_INFANTRY_ARMOR
        ].base_mineral_cost
        == 100
    )


def test_it_preserves_other_upgrade_settings(default_upgs):
    editor = RichUpgsEditor()
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
    updated = editor.set_upgrade_cost_setting(new_setting, default_upgs)
    for upgrade in _CLASSIC_UPGRADES:
        if upgrade == UpgradeId.TERRAN_INFANTRY_ARMOR:
            continue
        assert updated.upgrade_cost_settings[upgrade].base_mineral_cost == 100
