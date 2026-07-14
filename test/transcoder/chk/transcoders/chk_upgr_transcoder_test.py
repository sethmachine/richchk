import struct

from richchk.transcoder.chk.transcoders.chk_upgr_transcoder import ChkUpgrTranscoder

_NUM_PLAYERS = 12
_NUM_UPGRADES = 46
_PLAYER_UPGRADES_SIZE = _NUM_PLAYERS * _NUM_UPGRADES


def _build_upgr_binary(
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
    transcoder = ChkUpgrTranscoder()
    binary = _build_upgr_binary(player_max=3)
    section = transcoder.decode(binary)
    assert len(section.player_max_levels) == _PLAYER_UPGRADES_SIZE
    assert all(v == 3 for v in section.player_max_levels)


def test_it_decodes_expected_global_levels():
    transcoder = ChkUpgrTranscoder()
    binary = _build_upgr_binary(global_max=2, global_start=1)
    section = transcoder.decode(binary)
    assert len(section.global_max_levels) == _NUM_UPGRADES
    assert all(v == 2 for v in section.global_max_levels)
    assert all(v == 1 for v in section.global_start_levels)


def test_it_decodes_and_encodes_without_changing_data():
    transcoder = ChkUpgrTranscoder()
    binary = _build_upgr_binary()
    section = transcoder.decode(binary)
    encoded = transcoder.encode(section, include_header=False)
    assert encoded == binary


def test_it_decodes_and_encodes_mixed_values():
    transcoder = ChkUpgrTranscoder()
    player_max = list(range(_PLAYER_UPGRADES_SIZE % 256))[:_PLAYER_UPGRADES_SIZE]
    player_max = (player_max * (_PLAYER_UPGRADES_SIZE // len(player_max) + 1))[
        :_PLAYER_UPGRADES_SIZE
    ]
    player_start = [0] * _PLAYER_UPGRADES_SIZE
    global_max = [3] * _NUM_UPGRADES
    global_start = [0] * _NUM_UPGRADES
    player_defaults = [1] * _PLAYER_UPGRADES_SIZE
    binary = (
        struct.pack(f"{_PLAYER_UPGRADES_SIZE}B", *player_max)
        + struct.pack(f"{_PLAYER_UPGRADES_SIZE}B", *player_start)
        + struct.pack(f"{_NUM_UPGRADES}B", *global_max)
        + struct.pack(f"{_NUM_UPGRADES}B", *global_start)
        + struct.pack(f"{_PLAYER_UPGRADES_SIZE}B", *player_defaults)
    )
    section = transcoder.decode(binary)
    encoded = transcoder.encode(section, include_header=False)
    assert encoded == binary
