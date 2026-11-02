import pytest

from richchk.model.richchk.trig.extended_player_id import _ExtendedPlayerId
from richchk.model.richchk.trig.player_id import PlayerId
from richchk.transcoder.richchk.transcoders.helpers.richchk_player_id_transcoder import (
    RichChkPlayerIdTranscoder,
)


@pytest.mark.parametrize("named", list(PlayerId))
def test_it_decodes_named_values_to_the_enum_member(named):
    assert RichChkPlayerIdTranscoder.decode(named.id) is named


@pytest.mark.parametrize("value", [27, 255, 12746, 4294956727, 0xFFFFFFFF])
def test_it_decodes_other_values_to_an_extended_id(value):
    decoded = RichChkPlayerIdTranscoder.decode(value)
    assert decoded == _ExtendedPlayerId(value)


@pytest.mark.parametrize("value", [0, 11, 26, 27, 255, 4294956727, 0xFFFFFFFF])
def test_it_round_trips_every_kind_of_value(value):
    decoded = RichChkPlayerIdTranscoder.decode(value)
    assert RichChkPlayerIdTranscoder.encode(decoded) == value
