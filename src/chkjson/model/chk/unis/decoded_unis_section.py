"""UNIS - Unit Settings.

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

import dataclasses

from ...chk_section_name import ChkSectionName
from ..decoded_chk_section import DecodedChkSection


@dataclasses.dataclass(frozen=True)
class DecodedUnisSection(DecodedChkSection):

    # u8[228]: 1 byte for each unit, in order of Unit ID
    # 00 - Unit does not use default settings 01 - Unit does use default settings
    _unit_default_settings_flags: list[int]
    # u32[228]: Hit points for unit (Note the displayed value
    # is this value / 256, with the low byte being a fractional HP value)
    _unit_hitpoints: list[int]
    # u16[228]: Shield points, in order of Unit ID
    _unit_shieldpoints: list[int]
    # u8[228]: Armor points, in order of Unit ID
    _unit_armorpoints: list[int]
    # u16[228]: Build time (1/60 seconds), in order of Unit ID
    _unit_build_times: list[int]
    # u16[228]: Mineral cost, in order of Unit ID
    _unit_mineral_costs: list[int]
    # u16[228]: Gas cost, in order of Unit ID
    _unit_gas_costs: list[int]
    # u16[228]: String number, in order of Unit ID
    _unit_string_offsets: list[int]
    # u16[100]: Base weapon damage the weapon does,
    # in weapon ID order (#List of Unit Weapon# IDs)
    _unit_base_weapon_damages: list[int]
    # u16[100]: Upgrade bonus weapon damage, in weapon ID order
    _unit_upgrade_weapon_damages: list[int]

    @classmethod
    def section_name(cls) -> ChkSectionName:
        return ChkSectionName.UNIS

    @property
    def unit_default_settings_flags(self) -> list[int]:
        return self._unit_default_settings_flags.copy()

    @property
    def unit_hitpoints(self) -> list[int]:
        return self._unit_hitpoints.copy()

    @property
    def unit_shieldpoints(self) -> list[int]:
        return self._unit_shieldpoints.copy()

    @property
    def unit_armorpoints(self) -> list[int]:
        return self._unit_armorpoints.copy()

    @property
    def unit_build_times(self) -> list[int]:
        return self._unit_build_times.copy()

    @property
    def unit_mineral_costs(self) -> list[int]:
        return self._unit_mineral_costs.copy()

    @property
    def unit_gas_costs(self) -> list[int]:
        return self._unit_gas_costs.copy()

    @property
    def unit_string_offsets(self) -> list[int]:
        return self._unit_string_offsets.copy()

    @property
    def unit_base_weapon_damages(self) -> list[int]:
        return self._unit_base_weapon_damages.copy()

    @property
    def unit_upgrade_weapon_damages(self) -> list[int]:
        return self._unit_upgrade_weapon_damages.copy()
