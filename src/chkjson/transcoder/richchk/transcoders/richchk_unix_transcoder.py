"""Decode and encode the UNIx section which contains all unit settings.

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

u16[130]: Base weapon damage the weapon does, in weapon ID order (#List of Unit Weapon
IDs)

u16[130]: Upgrade bonus weapon damage, in weapon ID order
"""

from decimal import Decimal

from ....model.chk.unix.decoded_unix_section import DecodedUnixSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....model.richchk.str.rich_string import RichNullString
from ....model.richchk.unis.unit_id import UnitId
from ....model.richchk.unis.unit_setting import UnitSetting
from ....model.richchk.unis.unit_to_weapon_lookup import get_weapons_for_unit
from ....model.richchk.unis.weapon_id import WeaponId
from ....model.richchk.unis.weapon_setting import WeaponSetting
from ....model.richchk.unix.rich_unix_section import RichUnixSection
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)
from ....util import logger


class RichChkUnixTranscoder(
    RichChkSectionTranscoder[RichUnixSection, DecodedUnixSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedUnixSection.section_name(),
):
    # 100 weapons in vanilla SCM
    _NUM_WEAPONS = 130

    def __init__(self) -> None:
        self.log = logger.get_logger(RichChkUnixTranscoder.__name__)

    def decode(
        self,
        decoded_chk_section: DecodedUnixSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichUnixSection:
        unit_settings: list[UnitSetting] = []
        for unit_id, unit_uses_default_settings in enumerate(
            decoded_chk_section.unit_default_settings_flags
        ):
            unit_uses_default_settings_flag = True
            if not unit_uses_default_settings:
                unit_uses_default_settings_flag = False
            # issue with flake8 and black conflicting on max line length
            unit_name = rich_chk_decode_context.rich_str_lookup.get_string_by_id(
                decoded_chk_section.unit_string_ids[unit_id]
            )
            actual_unit_id: UnitId = UnitId.get_by_id(unit_id)
            unit_settings.append(
                UnitSetting(
                    _unit_id=actual_unit_id,
                    _hitpoints=self._compute_decode_hitpoints(
                        actual_unit_id, decoded_chk_section.unit_hitpoints[unit_id]
                    ),
                    _shieldpoints=decoded_chk_section.unit_shieldpoints[unit_id],
                    _armorpoints=decoded_chk_section.unit_armorpoints[unit_id],
                    _build_time=decoded_chk_section.unit_build_times[unit_id],
                    _mineral_cost=decoded_chk_section.unit_mineral_costs[unit_id],
                    _gas_cost=decoded_chk_section.unit_gas_costs[unit_id],
                    _custom_unit_name=unit_name,
                    _weapons=self._decode_weapons_for_unit_id(
                        UnitId.get_by_id(unit_id), decoded_chk_section
                    ),
                    _use_default_unit_settings=unit_uses_default_settings_flag,
                )
            )
        return RichUnixSection(
            _unit_settings=[
                x
                for x in unit_settings
                if not self._filter_unit_setting_if_all_values_unmodified(x)
            ]
        )

    def _compute_decode_hitpoints(
        self, unit_id: UnitId, hitpoints_before_decode: int
    ) -> Decimal:
        maybe_remainder = hitpoints_before_decode % 256
        if maybe_remainder:
            self.log.warning(
                not f"Unit {unit_id} "
                f"had fractional hitpoints of {maybe_remainder} / 256 "
                f"due to decoded hitpoints {hitpoints_before_decode}"
                f"not being an even multiple of 256"
            )
        actual_hitpoints = Decimal(hitpoints_before_decode) / Decimal(256)
        return actual_hitpoints

    def _decode_weapons_for_unit_id(
        self, unit_id: UnitId, decoded_chk_section: DecodedUnixSection
    ) -> list[WeaponSetting]:
        weapons: list[WeaponSetting] = []
        maybe_weapons: list[WeaponId] = get_weapons_for_unit(unit_id)
        if not maybe_weapons:
            self.log.info(
                f"No weapons found for unit {unit_id}.  "
                f"Verify this unit does not have any weapons."
            )
        for weapon_id in maybe_weapons:
            if weapon_id.id >= len(decoded_chk_section.unit_base_weapon_damages):
                continue
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

    def _filter_unit_setting_if_all_values_unmodified(
        self, unit_setting: UnitSetting
    ) -> bool:
        """Filter the unit setting from the RichUnis if it contains all unmodified
        values."""
        return (
            unit_setting.use_default_unit_settings
            and (unit_setting.hitpoints == 0)
            and (unit_setting.shieldpoints == 0)
            and (unit_setting.armorpoints == 0)
            and (unit_setting.mineral_cost == 0)
            and (unit_setting.gas_cost == 0)
            and (unit_setting.build_time == 0)
            and (isinstance(unit_setting.custom_unit_name, RichNullString))
        )

    def encode(
        self,
        rich_chk_section: RichUnixSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedUnixSection:
        unit_default_settings_flags = [1] * len(UnitId)
        hitpoints = [0] * len(UnitId)
        shieldpoints = [0] * len(UnitId)
        armorpoints = [0] * len(UnitId)
        build_times = [0] * len(UnitId)
        mineral_costs = [0] * len(UnitId)
        gas_costs = [0] * len(UnitId)
        string_ids = [0] * len(UnitId)
        base_weapon_damages = [0] * self._NUM_WEAPONS
        base_weapon_upgrades = [0] * self._NUM_WEAPONS

        for unit_setting in rich_chk_section.unit_settings:
            unit_default_settings_flags[unit_setting.unit_id.id] = int(
                unit_setting.use_default_unit_settings
            )
            hitpoints[unit_setting.unit_id.id] = int(
                Decimal(unit_setting.hitpoints) * Decimal(256)
            )
            shieldpoints[unit_setting.unit_id.id] = unit_setting.shieldpoints
            armorpoints[unit_setting.unit_id.id] = unit_setting.armorpoints
            build_times[unit_setting.unit_id.id] = unit_setting.build_time
            mineral_costs[unit_setting.unit_id.id] = unit_setting.mineral_cost
            gas_costs[unit_setting.unit_id.id] = unit_setting.gas_cost
            if isinstance(unit_setting.custom_unit_name, RichNullString):
                # units without modified names use 0 as their string ID
                string_ids[unit_setting.unit_id.id] = 0
            else:
                string_ids[
                    unit_setting.unit_id.id
                ] = rich_chk_encode_context.rich_str_lookup.get_id_by_string(
                    unit_setting.custom_unit_name
                )
            for weapon in unit_setting.weapons:
                base_weapon_damages[weapon.weapon_id.id] = weapon.base_damage
                base_weapon_upgrades[weapon.weapon_id.id] = weapon.upgrade_damage

        return DecodedUnixSection(
            _unit_default_settings_flags=unit_default_settings_flags,
            _unit_hitpoints=hitpoints,
            _unit_shieldpoints=shieldpoints,
            _unit_armorpoints=armorpoints,
            _unit_build_times=build_times,
            _unit_mineral_costs=mineral_costs,
            _unit_gas_costs=gas_costs,
            _unit_string_ids=string_ids,
            _unit_base_weapon_damages=base_weapon_damages,
            _unit_upgrade_weapon_damages=base_weapon_upgrades,
        )
