"""Editor for the PUNI - Player Unit Restrictions section."""

from ...model.richchk.puni.rich_puni_section import RichPuniSection
from ...model.richchk.trig.player_id import PlayerId
from ...model.richchk.unis.unit_id import UnitId


class RichPuniEditor:
    def set_unit_available_for_player(
        self,
        player: PlayerId,
        unit: UnitId,
        available: bool,
        puni: RichPuniSection,
    ) -> RichPuniSection:
        """Return a new section with the unit availability for a player updated.

        :param player: the player slot to update
        :param unit: the unit to update
        :param available: True=available, False=unavailable
        :param puni: the existing PUNI section
        :return: new RichPuniSection with the updated availability
        """
        updated = {p: dict(units) for p, units in puni.player_unit_availability.items()}
        updated[player][unit] = available
        updated_defaults = {
            p: dict(units) for p, units in puni.player_uses_defaults.items()
        }
        updated_defaults[player][unit] = False
        return RichPuniSection(
            _player_unit_availability=updated,
            _global_unit_availability=puni.global_unit_availability,
            _player_uses_defaults=updated_defaults,
        )

    def set_player_uses_default(
        self,
        player: PlayerId,
        unit: UnitId,
        uses_default: bool,
        puni: RichPuniSection,
    ) -> RichPuniSection:
        """Return a new section with the uses-default flag for a player/unit updated.

        :param player: the player slot to update
        :param unit: the unit to update
        :param uses_default: True=use global default, False=use player override
        :param puni: the existing PUNI section
        :return: new RichPuniSection with the updated flag
        """
        updated = {p: dict(units) for p, units in puni.player_uses_defaults.items()}
        updated[player][unit] = uses_default
        return RichPuniSection(
            _player_unit_availability=puni.player_unit_availability,
            _global_unit_availability=puni.global_unit_availability,
            _player_uses_defaults=updated,
        )

    def apply_player_unit_availability(
        self,
        updates: dict[PlayerId, dict[UnitId, bool]],
        puni: RichPuniSection,
    ) -> RichPuniSection:
        """Return a new section with per-player availability merged from a partial dict.

        Only the (player, unit) pairs present in `updates` are changed; all others are
        left as-is.  For each pair that appears in `updates`, player_uses_defaults is
        also set to False so the per-player value is actually consulted at runtime.

        :param updates: sparse mapping of player -> {unit -> available}
        :param puni: the existing PUNI section
        :return: new RichPuniSection with the merged overrides applied
        """
        new_availability = {
            p: dict(units) for p, units in puni.player_unit_availability.items()
        }
        new_defaults = {
            p: dict(units) for p, units in puni.player_uses_defaults.items()
        }
        for player, unit_map in updates.items():
            for unit, available in unit_map.items():
                new_availability[player][unit] = available
                new_defaults[player][unit] = False
        return RichPuniSection(
            _player_unit_availability=new_availability,
            _global_unit_availability=puni.global_unit_availability,
            _player_uses_defaults=new_defaults,
        )

    def set_unit_global_availability(
        self,
        unit: UnitId,
        available: bool,
        puni: RichPuniSection,
    ) -> RichPuniSection:
        """Return a new section with the global availability for a unit updated.

        :param unit: the unit to update
        :param available: True=available, False=unavailable
        :param puni: the existing PUNI section
        :return: new RichPuniSection with the updated global availability
        """
        updated = dict(puni.global_unit_availability)
        updated[unit] = available
        return RichPuniSection(
            _player_unit_availability=puni.player_unit_availability,
            _global_unit_availability=updated,
            _player_uses_defaults=puni.player_uses_defaults,
        )
