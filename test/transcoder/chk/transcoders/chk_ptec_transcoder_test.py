import struct

from richchk.transcoder.chk.transcoders.chk_ptec_transcoder import ChkPtecTranscoder

_NUM_PLAYERS = 12
_NUM_TECHS = 24
_PLAYER_TECHS_SIZE = _NUM_PLAYERS * _NUM_TECHS


def _build_ptec_binary(
    player_avail: int = 1,
    player_researched: int = 0,
    global_avail: int = 1,
    global_researched: int = 0,
    player_defaults: int = 1,
) -> bytes:
    data = struct.pack(f"{_PLAYER_TECHS_SIZE}B", *([player_avail] * _PLAYER_TECHS_SIZE))
    data += struct.pack(
        f"{_PLAYER_TECHS_SIZE}B", *([player_researched] * _PLAYER_TECHS_SIZE)
    )
    data += struct.pack(f"{_NUM_TECHS}B", *([global_avail] * _NUM_TECHS))
    data += struct.pack(f"{_NUM_TECHS}B", *([global_researched] * _NUM_TECHS))
    data += struct.pack(
        f"{_PLAYER_TECHS_SIZE}B", *([player_defaults] * _PLAYER_TECHS_SIZE)
    )
    return data


def test_it_decodes_expected_player_tech_availability():
    transcoder = ChkPtecTranscoder()
    binary = _build_ptec_binary(player_avail=1)
    section = transcoder.decode(binary)
    assert len(section.player_tech_availability) == _PLAYER_TECHS_SIZE
    assert all(v == 1 for v in section.player_tech_availability)


def test_it_decodes_expected_global_tech_availability():
    transcoder = ChkPtecTranscoder()
    binary = _build_ptec_binary(global_avail=0)
    section = transcoder.decode(binary)
    assert len(section.global_tech_availability) == _NUM_TECHS
    assert all(v == 0 for v in section.global_tech_availability)


def test_it_decodes_and_encodes_without_changing_data():
    transcoder = ChkPtecTranscoder()
    binary = _build_ptec_binary()
    section = transcoder.decode(binary)
    encoded = transcoder.encode(section, include_header=False)
    assert encoded == binary
