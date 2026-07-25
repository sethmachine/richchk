import struct

from richchk.transcoder.chk.transcoders.chk_tecx_transcoder import ChkTecxTranscoder

_NUM_TECHS = 44


def _build_tecx_binary(
    uses_default: int = 1,
    mineral: int = 100,
    gas: int = 0,
    time: int = 1800,
    energy: int = 0,
) -> bytes:
    data = struct.pack(f"{_NUM_TECHS}B", *([uses_default] * _NUM_TECHS))
    data += struct.pack(f"{_NUM_TECHS}H", *([mineral] * _NUM_TECHS))
    data += struct.pack(f"{_NUM_TECHS}H", *([gas] * _NUM_TECHS))
    data += struct.pack(f"{_NUM_TECHS}H", *([time] * _NUM_TECHS))
    data += struct.pack(f"{_NUM_TECHS}H", *([energy] * _NUM_TECHS))
    return data


def test_it_decodes_expected_uses_default_settings():
    transcoder = ChkTecxTranscoder()
    binary = _build_tecx_binary(uses_default=1)
    section = transcoder.decode(binary)
    assert len(section.uses_default_settings) == _NUM_TECHS
    assert all(v == 1 for v in section.uses_default_settings)


def test_it_decodes_expected_costs():
    transcoder = ChkTecxTranscoder()
    binary = _build_tecx_binary(mineral=200, gas=150, time=3600, energy=75)
    section = transcoder.decode(binary)
    assert all(v == 200 for v in section.mineral_cost)
    assert all(v == 150 for v in section.gas_cost)
    assert all(v == 3600 for v in section.research_time)
    assert all(v == 75 for v in section.energy_cost)


def test_it_decodes_and_encodes_without_changing_data():
    transcoder = ChkTecxTranscoder()
    binary = _build_tecx_binary()
    section = transcoder.decode(binary)
    encoded = transcoder.encode(section, include_header=False)
    assert encoded == binary


def test_it_decodes_and_encodes_with_varied_values():
    transcoder = ChkTecxTranscoder()
    uses_default = [i % 2 for i in range(_NUM_TECHS)]
    mineral = [i * 25 for i in range(_NUM_TECHS)]
    gas = [i * 10 for i in range(_NUM_TECHS)]
    time = [1800 + i * 100 for i in range(_NUM_TECHS)]
    energy = [50 + i * 5 for i in range(_NUM_TECHS)]
    binary = (
        struct.pack(f"{_NUM_TECHS}B", *uses_default)
        + struct.pack(f"{_NUM_TECHS}H", *mineral)
        + struct.pack(f"{_NUM_TECHS}H", *gas)
        + struct.pack(f"{_NUM_TECHS}H", *time)
        + struct.pack(f"{_NUM_TECHS}H", *energy)
    )
    section = transcoder.decode(binary)
    encoded = transcoder.encode(section, include_header=False)
    assert encoded == binary
