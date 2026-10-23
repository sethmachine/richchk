from typing import Optional

import pytest

from richchk.model.richchk.mrgn.rich_mrgn_lookup import RichMrgnLookup
from richchk.model.richchk.richchk_encode_context import RichChkEncodeContext
from richchk.model.richchk.str.rich_str_lookup import RichStrLookup
from richchk.model.richchk.swnm.rich_swnm_lookup import RichSwnmLookup
from richchk.model.richchk.trig.actions.preserve_trigger_action import PreserveTrigger
from richchk.model.richchk.trig.actions.set_deaths_action import SetDeathsAction
from richchk.model.richchk.trig.conditions.comparators.numeric_comparator import (
    NumericComparator,
)
from richchk.model.richchk.trig.conditions.deaths_condition import DeathsCondition
from richchk.model.richchk.trig.enums.amount_modifier import AmountModifier
from richchk.model.richchk.trig.player_id import PlayerId
from richchk.model.richchk.trig.rich_trig_section import RichTrigSection
from richchk.model.richchk.trig.rich_trigger import RichTrigger
from richchk.model.richchk.unis.unit_id import UnitId
from richchk.model.richchk.uprp.rich_cuwp_lookup import RichCuwpLookup
from richchk.transcoder.chk.transcoders.chk_trig_transcoder import ChkTrigTranscoder
from richchk.transcoder.richchk.transcoders.richchk_trig_transcoder import (
    RichChkTrigTranscoder,
)


def _context(optimize: bool) -> RichChkEncodeContext:
    return RichChkEncodeContext(
        _rich_str_lookup=RichStrLookup(
            _string_by_id_lookup={}, _id_by_string_lookup={}
        ),
        _rich_mrgn_lookup=RichMrgnLookup(
            _location_by_id_lookup={}, _id_by_location_lookup={}
        ),
        _rich_swnm_lookup=RichSwnmLookup(
            _switch_by_id_lookup={}, _id_by_switch_lookup={}
        ),
        _rich_cuwp_lookup=RichCuwpLookup(_cuwp_by_id_lookup={}, _id_by_cuwp_lookup={}),
        _optimize=optimize,
    )


def _trigger(
    i: int,
    unit: UnitId = UnitId.ZERG_SCOURGE,
    player: PlayerId = PlayerId.PLAYER_1,
    cond_amount: Optional[int] = None,
    act_amount: Optional[int] = None,
) -> RichTrigger:
    return RichTrigger(
        _conditions=[
            DeathsCondition(
                _group=PlayerId.PLAYER_8,
                _unit=unit,
                _comparator=NumericComparator.AT_LEAST,
                _amount=i if cond_amount is None else cond_amount,
            )
        ],
        _actions=[
            SetDeathsAction(
                _group=PlayerId.PLAYER_1,
                _unit=unit,
                _amount=i if act_amount is None else act_amount,
                _amount_modifier=AmountModifier.SET_TO,
            ),
            PreserveTrigger(),
        ],
        _players={player},
    )


def _encode(triggers: list, optimize: bool) -> bytes:
    section = RichTrigSection(_triggers=triggers)
    rich_encoded = RichChkTrigTranscoder().encode(section, _context(optimize))
    return bytes(ChkTrigTranscoder().encode(rich_encoded, include_header=False))


def _assert_matches_unoptimized(triggers: list) -> None:
    assert _encode(triggers, optimize=True) == _encode(triggers, optimize=False)


def _uniform(n: int = 5) -> list:
    return [_trigger(i) for i in range(1, n + 1)]


def test_uniform_batch_matches_unoptimized():
    _assert_matches_unoptimized(_uniform())


def test_non_uniform_batch_after_uniform_batch_matches_unoptimized():
    _assert_matches_unoptimized(_uniform())
    mixed = _uniform()
    mixed[2] = _trigger(3, unit=UnitId.ZERG_ZERGLING)
    _assert_matches_unoptimized(mixed)


def test_different_players_after_uniform_batch_matches_unoptimized():
    _assert_matches_unoptimized(_uniform())
    mixed = _uniform()
    mixed[1] = _trigger(2, player=PlayerId.PLAYER_2)
    _assert_matches_unoptimized(mixed)


def test_difference_beyond_first_200_triggers_is_encoded():
    triggers = [_trigger(i) for i in range(1, 301)]
    triggers[250] = _trigger(251, unit=UnitId.ZERG_ZERGLING)
    _assert_matches_unoptimized(triggers)


@pytest.mark.parametrize("cond_varies, act_varies", [(True, False), (False, True)])
def test_same_shape_with_different_varying_amounts_matches_unoptimized(
    cond_varies, act_varies
):
    def build(constant_cond: int, constant_act: int) -> list:
        return [
            _trigger(
                i,
                cond_amount=None if cond_varies else constant_cond,
                act_amount=None if act_varies else constant_act,
            )
            for i in range(1, 6)
        ]

    _assert_matches_unoptimized(build(7, 9))
    _assert_matches_unoptimized(build(8, 10))


def test_batches_in_either_order_give_the_same_bytes():
    uniform = _uniform()
    mixed = _uniform()
    mixed[4] = _trigger(5, unit=UnitId.ZERG_ZERGLING)
    expected_uniform = _encode(uniform, optimize=False)
    expected_mixed = _encode(mixed, optimize=False)
    assert _encode(mixed, optimize=True) == expected_mixed
    assert _encode(uniform, optimize=True) == expected_uniform
    assert _encode(mixed, optimize=True) == expected_mixed


def test_template_cache_does_not_leak_between_unrelated_lists():
    first = _uniform()
    _assert_matches_unoptimized(first)
    del first
    other = [_trigger(i, unit=UnitId.ZERG_ZERGLING) for i in range(1, 6)]
    _assert_matches_unoptimized(other)
