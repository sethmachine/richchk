import struct

from richchk.transcoder.chk.transcoders.chk_upgx_transcoder import ChkUpgxTranscoder

_NUM_UPGRADES = 61


def _build_upgx_binary(
    uses_default: int = 1,
    base_mineral: int = 100,
    mineral_factor: int = 100,
    base_gas: int = 0,
    gas_factor: int = 0,
    base_time: int = 1800,
    time_factor: int = 0,
) -> bytes:
    data = struct.pack(f"{_NUM_UPGRADES}B", *([uses_default] * _NUM_UPGRADES))
    data += struct.pack(f"{_NUM_UPGRADES}H", *([base_mineral] * _NUM_UPGRADES))
    data += struct.pack(f"{_NUM_UPGRADES}H", *([mineral_factor] * _NUM_UPGRADES))
    data += struct.pack(f"{_NUM_UPGRADES}H", *([base_gas] * _NUM_UPGRADES))
    data += struct.pack(f"{_NUM_UPGRADES}H", *([gas_factor] * _NUM_UPGRADES))
    data += struct.pack(f"{_NUM_UPGRADES}H", *([base_time] * _NUM_UPGRADES))
    data += struct.pack(f"{_NUM_UPGRADES}H", *([time_factor] * _NUM_UPGRADES))
    return data


def test_it_decodes_expected_uses_default_settings():
    transcoder = ChkUpgxTranscoder()
    binary = _build_upgx_binary(uses_default=1)
    section = transcoder.decode(binary)
    assert len(section.uses_default_settings) == _NUM_UPGRADES
    assert all(v == 1 for v in section.uses_default_settings)


def test_it_decodes_expected_costs():
    transcoder = ChkUpgxTranscoder()
    binary = _build_upgx_binary(base_mineral=200, mineral_factor=150, base_gas=100)
    section = transcoder.decode(binary)
    assert all(v == 200 for v in section.base_mineral_cost)
    assert all(v == 150 for v in section.mineral_cost_factor)
    assert all(v == 100 for v in section.base_gas_cost)


def test_it_decodes_and_encodes_without_changing_data():
    transcoder = ChkUpgxTranscoder()
    binary = _build_upgx_binary()
    section = transcoder.decode(binary)
    encoded = transcoder.encode(section, include_header=False)
    assert encoded == binary


def test_it_decodes_and_encodes_with_varied_values():
    transcoder = ChkUpgxTranscoder()
    uses_default = [i % 2 for i in range(_NUM_UPGRADES)]
    base_mineral = [i * 10 for i in range(_NUM_UPGRADES)]
    mineral_factor = [50] * _NUM_UPGRADES
    base_gas = [i * 5 for i in range(_NUM_UPGRADES)]
    gas_factor = [25] * _NUM_UPGRADES
    base_time = [1800] * _NUM_UPGRADES
    time_factor = [0] * _NUM_UPGRADES
    binary = (
        struct.pack(f"{_NUM_UPGRADES}B", *uses_default)
        + struct.pack(f"{_NUM_UPGRADES}H", *base_mineral)
        + struct.pack(f"{_NUM_UPGRADES}H", *mineral_factor)
        + struct.pack(f"{_NUM_UPGRADES}H", *base_gas)
        + struct.pack(f"{_NUM_UPGRADES}H", *gas_factor)
        + struct.pack(f"{_NUM_UPGRADES}H", *base_time)
        + struct.pack(f"{_NUM_UPGRADES}H", *time_factor)
    )
    section = transcoder.decode(binary)
    encoded = transcoder.encode(section, include_header=False)
    assert encoded == binary
