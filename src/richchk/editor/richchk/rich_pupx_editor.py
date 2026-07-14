"""Editor for the PUPx - Brood War Upgrade Restrictions section."""

from ...model.richchk.pupx.rich_pupx_section import RichPupxSection
from ...model.richchk.trig.player_id import PlayerId
from ...model.richchk.upgrades.upgrade_id import UpgradeId


class RichPupxEditor:
    def set_player_max_level(
        self,
        player: PlayerId,
        upgrade: UpgradeId,
        level: int,
        pupx: RichPupxSection,
    ) -> RichPupxSection:
        """Return a new section with the max upgrade level for a player updated.

        :param player: the player slot to update
        :param upgrade: the upgrade to update
        :param level: the new max level
        :param pupx: the existing PUPx section
        :return: new RichPupxSection with the updated max level
        """
        updated = {p: dict(upgrades) for p, upgrades in pupx.player_max_levels.items()}
        updated[player][upgrade] = level
        updated_defaults = {
            p: dict(upgrades) for p, upgrades in pupx.player_uses_defaults.items()
        }
        updated_defaults[player][upgrade] = False
        return RichPupxSection(
            _player_max_levels=updated,
            _player_start_levels=pupx.player_start_levels,
            _global_max_levels=pupx.global_max_levels,
            _global_start_levels=pupx.global_start_levels,
            _player_uses_defaults=updated_defaults,
        )

    def set_player_start_level(
        self,
        player: PlayerId,
        upgrade: UpgradeId,
        level: int,
        pupx: RichPupxSection,
    ) -> RichPupxSection:
        """Return a new section with the start upgrade level for a player updated.

        :param player: the player slot to update
        :param upgrade: the upgrade to update
        :param level: the new start level
        :param pupx: the existing PUPx section
        :return: new RichPupxSection with the updated start level
        """
        updated = {
            p: dict(upgrades) for p, upgrades in pupx.player_start_levels.items()
        }
        updated[player][upgrade] = level
        updated_defaults = {
            p: dict(upgrades) for p, upgrades in pupx.player_uses_defaults.items()
        }
        updated_defaults[player][upgrade] = False
        return RichPupxSection(
            _player_max_levels=pupx.player_max_levels,
            _player_start_levels=updated,
            _global_max_levels=pupx.global_max_levels,
            _global_start_levels=pupx.global_start_levels,
            _player_uses_defaults=updated_defaults,
        )

    def set_player_uses_default(
        self,
        player: PlayerId,
        upgrade: UpgradeId,
        uses_default: bool,
        pupx: RichPupxSection,
    ) -> RichPupxSection:
        """Return a new section with the uses-default flag for a player/upgrade updated.

        :param player: the player slot to update
        :param upgrade: the upgrade to update
        :param uses_default: True=use global default, False=use player override
        :param pupx: the existing PUPx section
        :return: new RichPupxSection with the updated flag
        """
        updated = {
            p: dict(upgrades) for p, upgrades in pupx.player_uses_defaults.items()
        }
        updated[player][upgrade] = uses_default
        return RichPupxSection(
            _player_max_levels=pupx.player_max_levels,
            _player_start_levels=pupx.player_start_levels,
            _global_max_levels=pupx.global_max_levels,
            _global_start_levels=pupx.global_start_levels,
            _player_uses_defaults=updated,
        )

    def apply_player_max_levels(
        self,
        updates: dict[PlayerId, dict[UpgradeId, int]],
        pupx: RichPupxSection,
    ) -> RichPupxSection:
        """Return a new section with per-player max levels merged from a partial dict.

        Only the (player, upgrade) pairs present in `updates` are changed; all others
        are left as-is.  player_uses_defaults is set to False for each pair so the per-
        player value is consulted at runtime.

        :param updates: sparse mapping of player -> {upgrade -> max level}
        :param pupx: the existing PUPx section
        :return: new RichPupxSection with the merged overrides applied
        """
        new_max = {p: dict(upgrades) for p, upgrades in pupx.player_max_levels.items()}
        new_defaults = {
            p: dict(upgrades) for p, upgrades in pupx.player_uses_defaults.items()
        }
        for player, upgrade_map in updates.items():
            for upgrade, level in upgrade_map.items():
                new_max[player][upgrade] = level
                new_defaults[player][upgrade] = False
        return RichPupxSection(
            _player_max_levels=new_max,
            _player_start_levels=pupx.player_start_levels,
            _global_max_levels=pupx.global_max_levels,
            _global_start_levels=pupx.global_start_levels,
            _player_uses_defaults=new_defaults,
        )

    def apply_player_start_levels(
        self,
        updates: dict[PlayerId, dict[UpgradeId, int]],
        pupx: RichPupxSection,
    ) -> RichPupxSection:
        """Return a new section with per-player start levels merged from a partial dict.

        Only the (player, upgrade) pairs present in `updates` are changed; all others
        are left as-is.  player_uses_defaults is set to False for each pair so the per-
        player value is consulted at runtime.

        :param updates: sparse mapping of player -> {upgrade -> start level}
        :param pupx: the existing PUPx section
        :return: new RichPupxSection with the merged overrides applied
        """
        new_start = {
            p: dict(upgrades) for p, upgrades in pupx.player_start_levels.items()
        }
        new_defaults = {
            p: dict(upgrades) for p, upgrades in pupx.player_uses_defaults.items()
        }
        for player, upgrade_map in updates.items():
            for upgrade, level in upgrade_map.items():
                new_start[player][upgrade] = level
                new_defaults[player][upgrade] = False
        return RichPupxSection(
            _player_max_levels=pupx.player_max_levels,
            _player_start_levels=new_start,
            _global_max_levels=pupx.global_max_levels,
            _global_start_levels=pupx.global_start_levels,
            _player_uses_defaults=new_defaults,
        )
