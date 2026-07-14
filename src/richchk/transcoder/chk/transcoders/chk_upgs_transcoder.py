"""Decode and encode UPGS - Classic Upgrade Settings.

u8[46]  uses_default_settings u16[46] base_mineral_cost u16[46] mineral_cost_factor
u16[46] base_gas_cost u16[46] gas_cost_factor u16[46] base_research_time u16[46]
research_time_factor

Total: 598 bytes.
"""

import struct
from io import BytesIO

from ....model.chk.upgs.decoded_upgs_section import DecodedUpgsSection
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder

_NUM_UPGRADES = 46


class ChkUpgsTranscoder(
    ChkSectionTranscoder[DecodedUpgsSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedUpgsSection.section_name(),
):
    def decode(self, chk_section_binary_data: bytes) -> DecodedUpgsSection:
        bytes_stream: BytesIO = BytesIO(chk_section_binary_data)
        uses_default_settings = list(
            struct.unpack(f"{_NUM_UPGRADES}B", bytes_stream.read(_NUM_UPGRADES))
        )
        base_mineral_cost = list(
            struct.unpack(f"{_NUM_UPGRADES}H", bytes_stream.read(_NUM_UPGRADES * 2))
        )
        mineral_cost_factor = list(
            struct.unpack(f"{_NUM_UPGRADES}H", bytes_stream.read(_NUM_UPGRADES * 2))
        )
        base_gas_cost = list(
            struct.unpack(f"{_NUM_UPGRADES}H", bytes_stream.read(_NUM_UPGRADES * 2))
        )
        gas_cost_factor = list(
            struct.unpack(f"{_NUM_UPGRADES}H", bytes_stream.read(_NUM_UPGRADES * 2))
        )
        base_research_time = list(
            struct.unpack(f"{_NUM_UPGRADES}H", bytes_stream.read(_NUM_UPGRADES * 2))
        )
        research_time_factor = list(
            struct.unpack(f"{_NUM_UPGRADES}H", bytes_stream.read(_NUM_UPGRADES * 2))
        )
        return DecodedUpgsSection(
            _uses_default_settings=uses_default_settings,
            _base_mineral_cost=base_mineral_cost,
            _mineral_cost_factor=mineral_cost_factor,
            _base_gas_cost=base_gas_cost,
            _gas_cost_factor=gas_cost_factor,
            _base_research_time=base_research_time,
            _research_time_factor=research_time_factor,
        )

    def _encode(self, decoded_chk_section: DecodedUpgsSection) -> bytes:
        data = struct.pack(
            f"{_NUM_UPGRADES}B", *decoded_chk_section.uses_default_settings
        )
        data += struct.pack(f"{_NUM_UPGRADES}H", *decoded_chk_section.base_mineral_cost)
        data += struct.pack(
            f"{_NUM_UPGRADES}H", *decoded_chk_section.mineral_cost_factor
        )
        data += struct.pack(f"{_NUM_UPGRADES}H", *decoded_chk_section.base_gas_cost)
        data += struct.pack(f"{_NUM_UPGRADES}H", *decoded_chk_section.gas_cost_factor)
        data += struct.pack(
            f"{_NUM_UPGRADES}H", *decoded_chk_section.base_research_time
        )
        data += struct.pack(
            f"{_NUM_UPGRADES}H", *decoded_chk_section.research_time_factor
        )
        return data
