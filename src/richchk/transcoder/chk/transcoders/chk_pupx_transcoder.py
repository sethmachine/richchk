"""Decode and encode PUPx - Brood War Upgrade Restrictions.

Same structure as UPGR but for 61 upgrades.

u8[12][61] player_max_upgrade_levels u8[12][61] player_start_upgrade_levels u8[61]
global_max_upgrade_levels u8[61]     global_start_upgrade_levels u8[12][61]
player_uses_defaults

Total: 2318 bytes.
"""

import struct
from io import BytesIO

from ....model.chk.pupx.decoded_pupx_section import DecodedPupxSection
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder

_NUM_PLAYERS = 12
_NUM_UPGRADES = 61
_PLAYER_UPGRADES_SIZE = _NUM_PLAYERS * _NUM_UPGRADES


class ChkPupxTranscoder(
    ChkSectionTranscoder[DecodedPupxSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedPupxSection.section_name(),
):
    def decode(self, chk_section_binary_data: bytes) -> DecodedPupxSection:
        bytes_stream: BytesIO = BytesIO(chk_section_binary_data)
        player_max_levels = list(
            struct.unpack(
                f"{_PLAYER_UPGRADES_SIZE}B", bytes_stream.read(_PLAYER_UPGRADES_SIZE)
            )
        )
        player_start_levels = list(
            struct.unpack(
                f"{_PLAYER_UPGRADES_SIZE}B", bytes_stream.read(_PLAYER_UPGRADES_SIZE)
            )
        )
        global_max_levels = list(
            struct.unpack(f"{_NUM_UPGRADES}B", bytes_stream.read(_NUM_UPGRADES))
        )
        global_start_levels = list(
            struct.unpack(f"{_NUM_UPGRADES}B", bytes_stream.read(_NUM_UPGRADES))
        )
        player_uses_defaults = list(
            struct.unpack(
                f"{_PLAYER_UPGRADES_SIZE}B", bytes_stream.read(_PLAYER_UPGRADES_SIZE)
            )
        )
        return DecodedPupxSection(
            _player_max_levels=player_max_levels,
            _player_start_levels=player_start_levels,
            _global_max_levels=global_max_levels,
            _global_start_levels=global_start_levels,
            _player_uses_defaults=player_uses_defaults,
        )

    def _encode(self, decoded_chk_section: DecodedPupxSection) -> bytes:
        data = struct.pack(
            f"{_PLAYER_UPGRADES_SIZE}B", *decoded_chk_section.player_max_levels
        )
        data += struct.pack(
            f"{_PLAYER_UPGRADES_SIZE}B", *decoded_chk_section.player_start_levels
        )
        data += struct.pack(f"{_NUM_UPGRADES}B", *decoded_chk_section.global_max_levels)
        data += struct.pack(
            f"{_NUM_UPGRADES}B", *decoded_chk_section.global_start_levels
        )
        data += struct.pack(
            f"{_PLAYER_UPGRADES_SIZE}B", *decoded_chk_section.player_uses_defaults
        )
        return data
