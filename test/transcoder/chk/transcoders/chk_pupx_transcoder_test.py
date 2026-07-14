import struct

from richchk.transcoder.chk.transcoders.chk_pupx_transcoder import ChkPupxTranscoder

_NUM_PLAYERS = 12
_NUM_UPGRADES = 61
_PLAYER_UPGRADES_SIZE = _NUM_PLAYERS * _NUM_UPGRADES


def _build_pupx_binary(
    player_max: int = 3,
    player_start: int = 0,
    global_max: int = 3,
    global_start: int = 0,
    player_defaults: int = 1,
) -> bytes:
    data = struct.pack(
        f"{_PLAYER_UPGRADES_SIZE}B", *([player_max] * _PLAYER_UPGRADES_SIZE)
    )
    data += struct.pack(
        f"{_PLAYER_UPGRADES_SIZE}B", *([player_start] * _PLAYER_UPGRADES_SIZE)
    )
    data += struct.pack(f"{_NUM_UPGRADES}B", *([global_max] * _NUM_UPGRADES))
    data += struct.pack(f"{_NUM_UPGRADES}B", *([global_start] * _NUM_UPGRADES))
    data += struct.pack(
        f"{_PLAYER_UPGRADES_SIZE}B", *([player_defaults] * _PLAYER_UPGRADES_SIZE)
    )
    return data


def test_it_decodes_expected_player_max_levels():
    transcoder = ChkPupxTranscoder()
    binary = _build_pupx_binary(player_max=3)
    section = transcoder.decode(binary)
    assert len(section.player_max_levels) == _PLAYER_UPGRADES_SIZE
    assert all(v == 3 for v in section.player_max_levels)


def test_it_decodes_expected_global_levels():
    transcoder = ChkPupxTranscoder()
    binary = _build_pupx_binary(global_max=2, global_start=1)
    section = transcoder.decode(binary)
    assert len(section.global_max_levels) == _NUM_UPGRADES
    assert all(v == 2 for v in section.global_max_levels)
    assert all(v == 1 for v in section.global_start_levels)


def test_it_decodes_and_encodes_without_changing_data():
    transcoder = ChkPupxTranscoder()
    binary = _build_pupx_binary()
    section = transcoder.decode(binary)
    encoded = transcoder.encode(section, include_header=False)
    assert encoded == binary


def test_binary_size_is_correct():
    binary = _build_pupx_binary()
    assert len(binary) == 2318
