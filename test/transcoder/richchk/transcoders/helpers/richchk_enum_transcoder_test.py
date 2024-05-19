import pytest

from chkjson.model.richchk.trig.player_id import PlayerId
from chkjson.model.richchk.unis.unit_id import UnitId
from chkjson.transcoder.richchk.transcoders.helpers.richchk_enum_transcoder import (
    RichChkEnumTranscoder,
)


def test_it_decodes_id_to_enum_instance():
    player_1_id = 0
    assert RichChkEnumTranscoder.decode_enum(player_1_id, PlayerId) == PlayerId.PLAYER_1


def test_it_builds_enum_id_map_after_first_usage():
    terran_marine_id = 0
    assert UnitId not in RichChkEnumTranscoder._ENUM_ID_MAP
    assert (
        RichChkEnumTranscoder.decode_enum(terran_marine_id, UnitId)
        == UnitId.TERRAN_MARINE
    )
    assert UnitId in RichChkEnumTranscoder._ENUM_ID_MAP
    assert set(RichChkEnumTranscoder._ENUM_ID_MAP[UnitId].values()) == set(
        [unit_id for unit_id in UnitId]
    )


def test_it_tells_if_enum_id_exists():
    player_2_id = 1
    too_high_player_id = 1337
    assert RichChkEnumTranscoder.contains_enum_by_id(player_2_id, PlayerId)
    assert not RichChkEnumTranscoder.contains_enum_by_id(too_high_player_id, PlayerId)


def test_it_throws_if_no_enum_for_id():
    too_high_player_id = 1337
    with pytest.raises(KeyError):
        RichChkEnumTranscoder.decode_enum(too_high_player_id, PlayerId)


def test_it_encodes_enum():
    assert RichChkEnumTranscoder.encode_enum(PlayerId.PLAYER_1) == 0
