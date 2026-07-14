"""Editor for the PUPx - Brood War Upgrade Restrictions section."""

from ...model.richchk.pupx.rich_pupx_section import RichPupxSection
from ...model.richchk.trig.player_id import PlayerId
from ...model.richchk.upgrades.upgrade_id import UpgradeId

_NUM_PLAYERS = 12
_NUM_UPGRADES = 61


class RichPupxEditor:
    def set_player_max_level(
        self,
        player: PlayerId,
        upgrade: UpgradeId,
        level: int,
        pupx: RichPupxSection,
    ) -> RichPupxSection:
        """Return a new section with the max upgrade level for a player updated.

        :param player: the player slot to update (PLAYER_1 through PLAYER_12)
        :param upgrade: the upgrade to update (must have id < 61)
        :param level: the new max level
        :param pupx: the existing PUPx section
        :return: new RichPupxSection with the updated max level
        """
        if player.id >= _NUM_PLAYERS:
            raise ValueError(
                f"player must be one of PLAYER_1 through PLAYER_12, got {player}"
            )
        if upgrade.id >= _NUM_UPGRADES:
            raise ValueError(
                f"upgrade id must be < {_NUM_UPGRADES} for PUPx, got {upgrade}"
            )
        updated = [row.copy() for row in pupx.player_max_levels]
        updated[player.id][upgrade.id] = level
        return RichPupxSection(
            _player_max_levels=updated,
            _player_start_levels=pupx.player_start_levels,
            _global_max_levels=pupx.global_max_levels,
            _global_start_levels=pupx.global_start_levels,
            _player_uses_defaults=pupx.player_uses_defaults,
        )

    def set_player_start_level(
        self,
        player: PlayerId,
        upgrade: UpgradeId,
        level: int,
        pupx: RichPupxSection,
    ) -> RichPupxSection:
        """Return a new section with the start upgrade level for a player updated.

        :param player: the player slot to update (PLAYER_1 through PLAYER_12)
        :param upgrade: the upgrade to update (must have id < 61)
        :param level: the new start level
        :param pupx: the existing PUPx section
        :return: new RichPupxSection with the updated start level
        """
        if player.id >= _NUM_PLAYERS:
            raise ValueError(
                f"player must be one of PLAYER_1 through PLAYER_12, got {player}"
            )
        if upgrade.id >= _NUM_UPGRADES:
            raise ValueError(
                f"upgrade id must be < {_NUM_UPGRADES} for PUPx, got {upgrade}"
            )
        updated = [row.copy() for row in pupx.player_start_levels]
        updated[player.id][upgrade.id] = level
        return RichPupxSection(
            _player_max_levels=pupx.player_max_levels,
            _player_start_levels=updated,
            _global_max_levels=pupx.global_max_levels,
            _global_start_levels=pupx.global_start_levels,
            _player_uses_defaults=pupx.player_uses_defaults,
        )

    def set_player_uses_default(
        self,
        player: PlayerId,
        upgrade: UpgradeId,
        uses_default: bool,
        pupx: RichPupxSection,
    ) -> RichPupxSection:
        """Return a new section with the uses-default flag for a player/upgrade updated.

        :param player: the player slot to update (PLAYER_1 through PLAYER_12)
        :param upgrade: the upgrade to update (must have id < 61)
        :param uses_default: True=use global default, False=use player override
        :param pupx: the existing PUPx section
        :return: new RichPupxSection with the updated flag
        """
        if player.id >= _NUM_PLAYERS:
            raise ValueError(
                f"player must be one of PLAYER_1 through PLAYER_12, got {player}"
            )
        if upgrade.id >= _NUM_UPGRADES:
            raise ValueError(
                f"upgrade id must be < {_NUM_UPGRADES} for PUPx, got {upgrade}"
            )
        updated = [row.copy() for row in pupx.player_uses_defaults]
        updated[player.id][upgrade.id] = uses_default
        return RichPupxSection(
            _player_max_levels=pupx.player_max_levels,
            _player_start_levels=pupx.player_start_levels,
            _global_max_levels=pupx.global_max_levels,
            _global_start_levels=pupx.global_start_levels,
            _player_uses_defaults=updated,
        )
