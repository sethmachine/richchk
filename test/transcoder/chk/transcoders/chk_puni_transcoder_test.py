import struct

from richchk.transcoder.chk.transcoders.chk_puni_transcoder import ChkPuniTranscoder

_NUM_PLAYERS = 12
_NUM_UNITS = 228
_PLAYER_UNITS_SIZE = _NUM_PLAYERS * _NUM_UNITS


def _build_puni_binary(
    player_availability: int = 1,
    global_availability: int = 1,
    player_defaults: int = 1,
) -> bytes:
    data = struct.pack(
        f"{_PLAYER_UNITS_SIZE}B", *([player_availability] * _PLAYER_UNITS_SIZE)
    )
    data += struct.pack(f"{_NUM_UNITS}B", *([global_availability] * _NUM_UNITS))
    data += struct.pack(
        f"{_PLAYER_UNITS_SIZE}B", *([player_defaults] * _PLAYER_UNITS_SIZE)
    )
    return data


def test_it_decodes_expected_player_unit_availability():
    transcoder = ChkPuniTranscoder()
    binary = _build_puni_binary(player_availability=1)
    section = transcoder.decode(binary)
    assert len(section.player_unit_availability) == _PLAYER_UNITS_SIZE
    assert all(v == 1 for v in section.player_unit_availability)


def test_it_decodes_expected_global_unit_availability():
    transcoder = ChkPuniTranscoder()
    binary = _build_puni_binary(global_availability=0)
    section = transcoder.decode(binary)
    assert len(section.global_unit_availability) == _NUM_UNITS
    assert all(v == 0 for v in section.global_unit_availability)


def test_it_decodes_expected_player_uses_defaults():
    transcoder = ChkPuniTranscoder()
    binary = _build_puni_binary(player_defaults=0)
    section = transcoder.decode(binary)
    assert len(section.player_uses_defaults) == _PLAYER_UNITS_SIZE
    assert all(v == 0 for v in section.player_uses_defaults)


def test_it_decodes_and_encodes_without_changing_data():
    transcoder = ChkPuniTranscoder()
    binary = _build_puni_binary()
    section = transcoder.decode(binary)
    encoded = transcoder.encode(section, include_header=False)
    assert encoded == binary


def test_it_decodes_and_encodes_mixed_values():
    transcoder = ChkPuniTranscoder()
    # player 0 all available, player 1 all unavailable, rest all available
    player_avail = (
        [1] * _NUM_UNITS
        + [0] * _NUM_UNITS
        + [1] * (_PLAYER_UNITS_SIZE - 2 * _NUM_UNITS)
    )
    global_avail = [1] * _NUM_UNITS
    player_defaults = [0] * _PLAYER_UNITS_SIZE
    binary = (
        struct.pack(f"{_PLAYER_UNITS_SIZE}B", *player_avail)
        + struct.pack(f"{_NUM_UNITS}B", *global_avail)
        + struct.pack(f"{_PLAYER_UNITS_SIZE}B", *player_defaults)
    )
    section = transcoder.decode(binary)
    encoded = transcoder.encode(section, include_header=False)
    assert encoded == binary
