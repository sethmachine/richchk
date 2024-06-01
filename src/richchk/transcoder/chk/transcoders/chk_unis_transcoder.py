"""Decode and encode the UNIS section which contains all unit settings.

Required for Vanilla and Hybrid (in Original mode). Not required for Melee. Validation:
Must be size of 4048 bytes. In Brood War scenarios, this section is replaced by "UNIx".

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

u16[100]: Base weapon damage the weapon does, in weapon ID order (#List of Unit Weapon
IDs)

u16[100]: Upgrade bonus weapon damage, in weapon ID order
"""

import struct
from io import BytesIO

from ....model.chk.unis.decoded_unis_section import DecodedUnisSection
from ....model.chk.unis.unis_constants import NUM_SCM_WEAPONS, NUM_UNITS
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder


class ChkUnisTranscoder(
    ChkSectionTranscoder[DecodedUnisSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedUnisSection.section_name(),
):
    def decode(self, chk_section_binary_data: bytes) -> DecodedUnisSection:
        bytes_stream: BytesIO = BytesIO(chk_section_binary_data)
        use_settings_flags = [
            struct.unpack("B", bytes_stream.read(1))[0] for _ in range(NUM_UNITS)
        ]
        hitpoints = [
            struct.unpack("I", bytes_stream.read(4))[0] for _ in range(NUM_UNITS)
        ]
        shields = [
            struct.unpack("H", bytes_stream.read(2))[0] for _ in range(NUM_UNITS)
        ]
        armor = [struct.unpack("B", bytes_stream.read(1))[0] for _ in range(NUM_UNITS)]
        build_time = [
            struct.unpack("H", bytes_stream.read(2))[0] for _ in range(NUM_UNITS)
        ]
        minerals = [
            struct.unpack("H", bytes_stream.read(2))[0] for _ in range(NUM_UNITS)
        ]
        gas = [struct.unpack("H", bytes_stream.read(2))[0] for _ in range(NUM_UNITS)]
        string_ids = [
            struct.unpack("H", bytes_stream.read(2))[0] for _ in range(NUM_UNITS)
        ]
        weapon_damage = [
            struct.unpack("H", bytes_stream.read(2))[0] for _ in range(NUM_SCM_WEAPONS)
        ]
        weapon_bonus = [
            struct.unpack("H", bytes_stream.read(2))[0] for _ in range(NUM_SCM_WEAPONS)
        ]
        return DecodedUnisSection(
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

    def _encode(self, decoded_chk_section: DecodedUnisSection) -> bytes:
        data: bytes = b""
        data += struct.pack(
            "{}B".format(NUM_UNITS), *decoded_chk_section.unit_default_settings_flags
        )
        data += struct.pack(
            "{}I".format(NUM_UNITS), *decoded_chk_section.unit_hitpoints
        )
        data += struct.pack(
            "{}H".format(NUM_UNITS), *decoded_chk_section.unit_shieldpoints
        )
        data += struct.pack(
            "{}B".format(NUM_UNITS), *decoded_chk_section.unit_armorpoints
        )
        data += struct.pack(
            "{}H".format(NUM_UNITS), *decoded_chk_section.unit_build_times
        )
        data += struct.pack(
            "{}H".format(NUM_UNITS), *decoded_chk_section.unit_mineral_costs
        )
        data += struct.pack(
            "{}H".format(NUM_UNITS), *decoded_chk_section.unit_gas_costs
        )
        data += struct.pack(
            "{}H".format(NUM_UNITS), *decoded_chk_section.unit_string_ids
        )
        data += struct.pack(
            "{}H".format(NUM_SCM_WEAPONS), *decoded_chk_section.unit_base_weapon_damages
        )
        data += struct.pack(
            "{}H".format(NUM_SCM_WEAPONS),
            *decoded_chk_section.unit_upgrade_weapon_damages
        )
        return data
