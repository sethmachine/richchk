import logging

import pytest

from richchk.model.richchk.trig.extended_player_id import _ExtendedPlayerId
from richchk.model.richchk.trig.player_id import PlayerId


def test_it_accepts_values_beyond_the_named_player_ids_up_to_the_u32_limit():
    assert _ExtendedPlayerId(27).id == 27
    assert _ExtendedPlayerId(255).id == 255
    assert _ExtendedPlayerId(0xFFFFFFFF).id == 0xFFFFFFFF


@pytest.mark.parametrize("named", list(PlayerId))
def test_it_rejects_every_named_player_id_and_points_to_the_named_one(named, caplog):
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError, match="named player ID"):
            _ExtendedPlayerId(named.id)
    assert any(str(named) in r.getMessage() for r in caplog.records)


@pytest.mark.parametrize("value", [0x100000000, 2**40, -1])
def test_it_rejects_values_that_do_not_fit_in_a_u32_and_logs_why(value, caplog):
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError, match="cannot exceed 4294967295"):
            _ExtendedPlayerId(value)
    assert any("u32" in r.getMessage() for r in caplog.records)


def test_it_is_equal_and_hashes_by_value():
    assert _ExtendedPlayerId(500) == _ExtendedPlayerId(500)
    assert hash(_ExtendedPlayerId(500)) == hash(_ExtendedPlayerId(500))
    assert _ExtendedPlayerId(500) != _ExtendedPlayerId(501)
    assert _ExtendedPlayerId(27) != PlayerId.PLAYER_1
