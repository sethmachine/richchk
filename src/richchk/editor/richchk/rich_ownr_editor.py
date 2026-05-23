"""Editor for the OWNR - StarCraft Player Types section."""

from ...model.richchk.ownr.player_controller import PlayerController
from ...model.richchk.ownr.rich_ownr_section import RichOwnrSection

_NUM_PLAYERS = 12


class RichOwnrEditor:
    def set_player_controller(
        self,
        player_slot: int,
        controller: PlayerController,
        ownr: RichOwnrSection,
    ) -> RichOwnrSection:
        """Return a new section with the controller for a single player slot replaced.

        :param player_slot: zero-based player slot index (0-11)
        :param controller: the PlayerController to assign
        :param ownr: the existing OWNR section
        :return: new RichOwnrSection with the updated controller
        """
        if player_slot < 0 or player_slot >= _NUM_PLAYERS:
            raise ValueError(
                f"player_slot must be in range [0, {_NUM_PLAYERS - 1}], got {player_slot}"
            )
        updated = list(ownr.player_controllers)
        updated[player_slot] = controller
        return RichOwnrSection(_player_controllers=updated)

    def set_all_player_controllers(
        self,
        controllers: list[PlayerController],
        ownr: RichOwnrSection,
    ) -> RichOwnrSection:
        """Return a new section with all player controllers replaced.

        :param controllers: list of exactly 12 PlayerController values
        :param ownr: the existing OWNR section
        :return: new RichOwnrSection with the updated controllers
        """
        if len(controllers) != _NUM_PLAYERS:
            raise ValueError(
                f"controllers must have exactly {_NUM_PLAYERS} entries, got {len(controllers)}"
            )
        return RichOwnrSection(_player_controllers=list(controllers))
