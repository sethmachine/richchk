"""Editor for the OWNR - StarCraft Player Types section."""

from ...model.richchk.ownr.player_type import PlayerType
from ...model.richchk.ownr.rich_ownr_section import RichOwnrSection
from ...model.richchk.trig.player_id import PlayerId

_NUM_PLAYERS = 12


class RichOwnrEditor:
    def set_player_type(
        self,
        player: PlayerId,
        player_type: PlayerType,
        ownr: RichOwnrSection,
    ) -> RichOwnrSection:
        """Return a new section with the type for a single player slot replaced.

        :param player: the player slot to update (PLAYER_1 through PLAYER_12)
        :param player_type: the PlayerType to assign
        :param ownr: the existing OWNR section
        :return: new RichOwnrSection with the updated type
        """
        if player.id >= _NUM_PLAYERS:
            raise ValueError(
                f"player must be one of PLAYER_1 through PLAYER_12, got {player}"
            )
        updated = list(ownr.player_types)
        updated[player.id] = player_type
        return RichOwnrSection(_player_types=updated)

    def set_player_types(
        self,
        player_types: dict[PlayerId, PlayerType],
        ownr: RichOwnrSection,
    ) -> RichOwnrSection:
        """Return a new section with the given player types updated.

        :param player_types: mapping of player slots to update; slots absent from the
            dict retain their existing type
        :param ownr: the existing OWNR section
        :return: new RichOwnrSection with the updated types
        """
        updated = list(ownr.player_types)
        for player, player_type in player_types.items():
            updated[player.id] = player_type
        return RichOwnrSection(_player_types=updated)
