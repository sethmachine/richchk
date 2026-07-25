"""Decode and encode PTEx - Brood War Tech Restrictions.

u8[12][44] player_tech_availability u8[12][44] player_tech_researched u8[44]
global_tech_availability u8[44]     global_tech_researched u8[12][44]
player_uses_defaults

Total: 1672 bytes.
"""

import struct
from io import BytesIO

from ....model.chk.ptex.decoded_ptex_section import DecodedPtexSection
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder

_NUM_PLAYERS = 12
_NUM_TECHS = 44
_PLAYER_TECHS_SIZE = _NUM_PLAYERS * _NUM_TECHS


class ChkPtexTranscoder(
    ChkSectionTranscoder[DecodedPtexSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedPtexSection.section_name(),
):
    def decode(self, chk_section_binary_data: bytes) -> DecodedPtexSection:
        bytes_stream: BytesIO = BytesIO(chk_section_binary_data)
        player_tech_availability = list(
            struct.unpack(
                f"{_PLAYER_TECHS_SIZE}B", bytes_stream.read(_PLAYER_TECHS_SIZE)
            )
        )
        player_tech_researched = list(
            struct.unpack(
                f"{_PLAYER_TECHS_SIZE}B", bytes_stream.read(_PLAYER_TECHS_SIZE)
            )
        )
        global_tech_availability = list(
            struct.unpack(f"{_NUM_TECHS}B", bytes_stream.read(_NUM_TECHS))
        )
        global_tech_researched = list(
            struct.unpack(f"{_NUM_TECHS}B", bytes_stream.read(_NUM_TECHS))
        )
        player_uses_defaults = list(
            struct.unpack(
                f"{_PLAYER_TECHS_SIZE}B", bytes_stream.read(_PLAYER_TECHS_SIZE)
            )
        )
        return DecodedPtexSection(
            _player_tech_availability=player_tech_availability,
            _player_tech_researched=player_tech_researched,
            _global_tech_availability=global_tech_availability,
            _global_tech_researched=global_tech_researched,
            _player_uses_defaults=player_uses_defaults,
        )

    def _encode(self, decoded_chk_section: DecodedPtexSection) -> bytes:
        data = struct.pack(
            f"{_PLAYER_TECHS_SIZE}B", *decoded_chk_section.player_tech_availability
        )
        data += struct.pack(
            f"{_PLAYER_TECHS_SIZE}B", *decoded_chk_section.player_tech_researched
        )
        data += struct.pack(
            f"{_NUM_TECHS}B", *decoded_chk_section.global_tech_availability
        )
        data += struct.pack(
            f"{_NUM_TECHS}B", *decoded_chk_section.global_tech_researched
        )
        data += struct.pack(
            f"{_PLAYER_TECHS_SIZE}B", *decoded_chk_section.player_uses_defaults
        )
        return data
