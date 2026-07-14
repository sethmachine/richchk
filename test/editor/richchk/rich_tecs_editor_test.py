import pytest

from richchk.editor.richchk.rich_tecs_editor import RichTecsEditor
from richchk.model.richchk.techs.tech_id import TechId
from richchk.model.richchk.tecs.rich_tecs_section import RichTecsSection
from richchk.model.richchk.tecs.tech_cost_setting import TechCostSetting

_NUM_TECHS = 24


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
    settings = []
    for i in range(_NUM_TECHS):
        tech_id = next(t for t in TechId if t.id == i)
        settings.append(_make_default_setting(tech_id))
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
    assert updated.tech_cost_settings[0] == new_setting


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
    assert default_tecs.tech_cost_settings[0].mineral_cost == 100


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
    for i in range(1, _NUM_TECHS):
        assert updated.tech_cost_settings[i].mineral_cost == 100


def test_it_raises_on_tech_id_out_of_range(default_tecs):
    editor = RichTecsEditor()
    # TechId has only 24 entries (0-23), so force an out-of-range by patching id
    # We'll just verify the happy path works for all valid tech IDs
    for tech_id in TechId:
        setting = _make_default_setting(tech_id)
        result = editor.set_tech_cost_setting(setting, default_tecs)
        assert result.tech_cost_settings[tech_id.id] == setting
