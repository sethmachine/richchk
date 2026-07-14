"""Decode and encode TECS - Classic Tech Settings.

u8[24]  uses_default_settings u16[24] mineral_cost u16[24] gas_cost u16[24]
research_time u16[24] energy_cost

Total: 216 bytes.
"""

import struct
from io import BytesIO

from ....model.chk.tecs.decoded_tecs_section import DecodedTecsSection
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder

_NUM_TECHS = 24


class ChkTecsTranscoder(
    ChkSectionTranscoder[DecodedTecsSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedTecsSection.section_name(),
):
    def decode(self, chk_section_binary_data: bytes) -> DecodedTecsSection:
        bytes_stream: BytesIO = BytesIO(chk_section_binary_data)
        uses_default_settings = list(
            struct.unpack(f"{_NUM_TECHS}B", bytes_stream.read(_NUM_TECHS))
        )
        mineral_cost = list(
            struct.unpack(f"{_NUM_TECHS}H", bytes_stream.read(_NUM_TECHS * 2))
        )
        gas_cost = list(
            struct.unpack(f"{_NUM_TECHS}H", bytes_stream.read(_NUM_TECHS * 2))
        )
        research_time = list(
            struct.unpack(f"{_NUM_TECHS}H", bytes_stream.read(_NUM_TECHS * 2))
        )
        energy_cost = list(
            struct.unpack(f"{_NUM_TECHS}H", bytes_stream.read(_NUM_TECHS * 2))
        )
        return DecodedTecsSection(
            _uses_default_settings=uses_default_settings,
            _mineral_cost=mineral_cost,
            _gas_cost=gas_cost,
            _research_time=research_time,
            _energy_cost=energy_cost,
        )

    def _encode(self, decoded_chk_section: DecodedTecsSection) -> bytes:
        data = struct.pack(f"{_NUM_TECHS}B", *decoded_chk_section.uses_default_settings)
        data += struct.pack(f"{_NUM_TECHS}H", *decoded_chk_section.mineral_cost)
        data += struct.pack(f"{_NUM_TECHS}H", *decoded_chk_section.gas_cost)
        data += struct.pack(f"{_NUM_TECHS}H", *decoded_chk_section.research_time)
        data += struct.pack(f"{_NUM_TECHS}H", *decoded_chk_section.energy_cost)
        return data
