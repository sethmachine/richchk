import pytest

from richchk.editor.richchk.rich_tecs_editor import RichTecsEditor
from richchk.model.richchk.techs.tech_id import TechId
from richchk.model.richchk.tecs.rich_tecs_section import RichTecsSection
from richchk.model.richchk.tecs.tech_cost_setting import TechCostSetting

_TECHS = list(TechId)


def _make_default_setting(tech_id: TechId) -> TechCostSetting:
    return TechCostSetting(
        _tech_id=tech_id,
        _uses_default_settings=True,
        _mineral_cost=100,
        _gas_cost=0,
        _research_time=1800,
        _energy_cost=0,
    )


def _make_tecs() -> RichTecsSection:
    settings = {tech: _make_default_setting(tech) for tech in _TECHS}
    return RichTecsSection(_tech_cost_settings=settings)


@pytest.fixture
def default_tecs() -> RichTecsSection:
    return _make_tecs()


def test_it_sets_tech_cost_setting(default_tecs):
    editor = RichTecsEditor()
    new_setting = TechCostSetting(
        _tech_id=TechId.STIM_PACKS,
        _uses_default_settings=False,
        _mineral_cost=0,
        _gas_cost=0,
        _research_time=900,
        _energy_cost=10,
    )
    updated = editor.set_tech_cost_setting(new_setting, default_tecs)
    assert updated.tech_cost_settings[TechId.STIM_PACKS] == new_setting


def test_it_does_not_mutate_original(default_tecs):
    editor = RichTecsEditor()
    new_setting = TechCostSetting(
        _tech_id=TechId.STIM_PACKS,
        _uses_default_settings=False,
        _mineral_cost=999,
        _gas_cost=999,
        _research_time=9999,
        _energy_cost=999,
    )
    editor.set_tech_cost_setting(new_setting, default_tecs)
    assert default_tecs.tech_cost_settings[TechId.STIM_PACKS].mineral_cost == 100


def test_it_preserves_other_tech_settings(default_tecs):
    editor = RichTecsEditor()
    new_setting = TechCostSetting(
        _tech_id=TechId.STIM_PACKS,
        _uses_default_settings=False,
        _mineral_cost=999,
        _gas_cost=999,
        _research_time=9999,
        _energy_cost=999,
    )
    updated = editor.set_tech_cost_setting(new_setting, default_tecs)
    for tech in _TECHS:
        if tech == TechId.STIM_PACKS:
            continue
        assert updated.tech_cost_settings[tech].mineral_cost == 100


def test_apply_tech_cost_settings_merges_partial_dict(default_tecs):
    editor = RichTecsEditor()
    new_stim = TechCostSetting(
        _tech_id=TechId.STIM_PACKS,
        _uses_default_settings=False,
        _mineral_cost=0,
        _gas_cost=0,
        _research_time=900,
        _energy_cost=10,
    )
    new_lockdown = TechCostSetting(
        _tech_id=TechId.LOCKDOWN,
        _uses_default_settings=False,
        _mineral_cost=200,
        _gas_cost=200,
        _research_time=1800,
        _energy_cost=100,
    )
    updates = {TechId.STIM_PACKS: new_stim, TechId.LOCKDOWN: new_lockdown}
    updated = editor.apply_tech_cost_settings(updates, default_tecs)
    assert updated.tech_cost_settings[TechId.STIM_PACKS] == new_stim
    assert updated.tech_cost_settings[TechId.LOCKDOWN] == new_lockdown
    assert updated.tech_cost_settings[TechId.ARCHON_WARP].mineral_cost == 100


def test_apply_tech_cost_settings_does_not_mutate_original(default_tecs):
    editor = RichTecsEditor()
    new_stim = TechCostSetting(
        _tech_id=TechId.STIM_PACKS,
        _uses_default_settings=False,
        _mineral_cost=999,
        _gas_cost=999,
        _research_time=9999,
        _energy_cost=999,
    )
    editor.apply_tech_cost_settings({TechId.STIM_PACKS: new_stim}, default_tecs)
    assert default_tecs.tech_cost_settings[TechId.STIM_PACKS].mineral_cost == 100
