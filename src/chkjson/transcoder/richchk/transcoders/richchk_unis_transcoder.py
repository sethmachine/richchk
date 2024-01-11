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

from ....model.chk.unis.decoded_unis_section import DecodedUnisSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.unis.rich_unis_section import RichUnisSection
from ....model.richchk.unis.unit_id import UnitId
from ....model.richchk.unis.unit_setting import UnitSetting
from ....model.richchk.unis.unit_to_weapon_lookup import get_weapons_for_unit
from ....model.richchk.unis.weapon_id import WeaponId
from ....model.richchk.unis.weapon_setting import WeaponSetting
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)
from ....util import logger


class RichChkUnisTranscoder(
    RichChkSectionTranscoder[RichUnisSection, DecodedUnisSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedUnisSection.section_name(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(RichChkUnisTranscoder.__name__)

    def decode(
        self,
        decoded_chk_section: DecodedUnisSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichUnisSection:
        unit_settings: list[UnitSetting] = []
        for unit_id, unit_uses_default_settings in enumerate(
            decoded_chk_section.unit_default_settings_flags
        ):
            if not unit_uses_default_settings:
                # issue with flake8 and black conflicting on max line length
                unit_name = rich_chk_decode_context.rich_str_lookup.get_string_by_id(
                    decoded_chk_section.unit_string_ids[unit_id]
                )
                unit_settings.append(
                    UnitSetting(
                        _unit_id=UnitId.get_by_id(unit_id),
                        _hitpoints=decoded_chk_section.unit_hitpoints[unit_id] // 256,
                        _shieldpoints=decoded_chk_section.unit_shieldpoints[unit_id],
                        _armorpoints=decoded_chk_section.unit_armorpoints[unit_id],
                        _build_time=decoded_chk_section.unit_build_times[unit_id],
                        _mineral_cost=decoded_chk_section.unit_mineral_costs[unit_id],
                        _gas_cost=decoded_chk_section.unit_gas_costs[unit_id],
                        _custom_unit_name=unit_name,
                        _weapons=self._decode_weapons_for_unit_id(
                            UnitId.get_by_id(unit_id), decoded_chk_section
                        ),
                    )
                )
        return RichUnisSection(_unit_settings=unit_settings)

    def _decode_weapons_for_unit_id(
        self, unit_id: UnitId, decoded_chk_section: DecodedUnisSection
    ) -> list[WeaponSetting]:
        weapons: list[WeaponSetting] = []
        maybe_weapons: list[WeaponId] = get_weapons_for_unit(unit_id)
        if not maybe_weapons:
            self.log.info(
                f"No weapons found for unit {unit_id}.  "
                f"Verify this unit does not have any weapons."
            )
        for weapon_id in maybe_weapons:
            weapons.append(
                WeaponSetting(
                    _weapon_id=weapon_id,
                    _base_damage=decoded_chk_section.unit_base_weapon_damages[
                        weapon_id.id
                    ],
                    _upgrade_damage=decoded_chk_section.unit_upgrade_weapon_damages[
                        weapon_id.id
                    ],
                )
            )
        return weapons

    def encode(self, rich_chk_section: RichUnisSection) -> DecodedUnisSection:
        return DecodedUnisSection([], [], [], [], [], [], [], [], [], [])
