"""Decode and encode the UNIx section which contains all Brood War unit settings.

Required for Hybrid (in Expansion mode) and Brood War. Not required for Melee.
Validation: Must be size of 4168 bytes. In Brood War scenarios this section replaces
"UNIS".

This section is identical to UNIS section except it uses the Brood War set of 130
weapons instead of the original 100.

This section contains the unit settings for the level:

u8[228]: 1 byte for each unit, in order of Unit ID

00 - Unit does not use default settings 01 - Unit does use default settings

u32[228]: Hit points for unit (Note the displayed value is this value / 256, with the
low byte being a fractional HP value)

u16[228]: Shield points, in order of Unit ID

u8[228]: Armor points, in order of Unit ID

u16[228]: Build time (1/60 seconds), in order of Unit ID

u16[228]: Mineral cost, in order of Unit ID

u16[228]: Gas cost, in order of Unit ID

u16[228]: String number, in order of Unit ID

u16[130]: Base weapon damage the weapon does, in weapon ID order (#List of Unit Weapon
IDs)

u16[130]: Upgrade bonus weapon damage, in weapon ID order
"""

import struct
from io import BytesIO

from ....model.chk.unix.decoded_unix_section import DecodedUnixSection
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder


class ChkUnixTranscoder(
    ChkSectionTranscoder[DecodedUnixSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedUnixSection.section_name(),
):
    _NUM_UNITS = 228
    _NUM_WEAPONS = 130

    def decode(self, chk_section_binary_data: bytes) -> DecodedUnixSection:
        bytes_stream: BytesIO = BytesIO(chk_section_binary_data)
        use_settings_flags = [
            struct.unpack("B", bytes_stream.read(1))[0] for _ in range(self._NUM_UNITS)
        ]
        hitpoints = [
            struct.unpack("I", bytes_stream.read(4))[0] for _ in range(self._NUM_UNITS)
        ]
        shields = [
            struct.unpack("H", bytes_stream.read(2))[0] for _ in range(self._NUM_UNITS)
        ]
        armor = [
            struct.unpack("B", bytes_stream.read(1))[0] for _ in range(self._NUM_UNITS)
        ]
        build_time = [
            struct.unpack("H", bytes_stream.read(2))[0] for _ in range(self._NUM_UNITS)
        ]
        minerals = [
            struct.unpack("H", bytes_stream.read(2))[0] for _ in range(self._NUM_UNITS)
        ]
        gas = [
            struct.unpack("H", bytes_stream.read(2))[0] for _ in range(self._NUM_UNITS)
        ]
        string_ids = [
            struct.unpack("H", bytes_stream.read(2))[0] for _ in range(self._NUM_UNITS)
        ]
        weapon_damage = [
            struct.unpack("H", bytes_stream.read(2))[0]
            for _ in range(self._NUM_WEAPONS)
        ]
        weapon_bonus = [
            struct.unpack("H", bytes_stream.read(2))[0]
            for _ in range(self._NUM_WEAPONS)
        ]
        return DecodedUnixSection(
            _unit_default_settings_flags=use_settings_flags,
            _unit_hitpoints=hitpoints,
            _unit_shieldpoints=shields,
            _unit_armorpoints=armor,
            _unit_build_times=build_time,
            _unit_mineral_costs=minerals,
            _unit_gas_costs=gas,
            _unit_string_ids=string_ids,
            _unit_base_weapon_damages=weapon_damage,
            _unit_upgrade_weapon_damages=weapon_bonus,
        )

    def _encode(self, decoded_chk_section: DecodedUnixSection) -> bytes:
        data: bytes = b""
        data += struct.pack(
            "{}B".format(self._NUM_UNITS),
            *decoded_chk_section.unit_default_settings_flags
        )
        data += struct.pack(
            "{}I".format(self._NUM_UNITS), *decoded_chk_section.unit_hitpoints
        )
        data += struct.pack(
            "{}H".format(self._NUM_UNITS), *decoded_chk_section.unit_shieldpoints
        )
        data += struct.pack(
            "{}B".format(self._NUM_UNITS), *decoded_chk_section.unit_armorpoints
        )
        data += struct.pack(
            "{}H".format(self._NUM_UNITS), *decoded_chk_section.unit_build_times
        )
        data += struct.pack(
            "{}H".format(self._NUM_UNITS), *decoded_chk_section.unit_mineral_costs
        )
        data += struct.pack(
            "{}H".format(self._NUM_UNITS), *decoded_chk_section.unit_gas_costs
        )
        data += struct.pack(
            "{}H".format(self._NUM_UNITS), *decoded_chk_section.unit_string_ids
        )
        data += struct.pack(
            "{}H".format(self._NUM_WEAPONS),
            *decoded_chk_section.unit_base_weapon_damages
        )
        data += struct.pack(
            "{}H".format(self._NUM_WEAPONS),
            *decoded_chk_section.unit_upgrade_weapon_damages
        )
        return data
