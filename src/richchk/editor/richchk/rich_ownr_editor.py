"""Editor for the OWNR - StarCraft Player Types section."""

from ...model.richchk.ownr.player_type import PlayerType
from ...model.richchk.ownr.rich_ownr_section import RichOwnrSection
from ...model.richchk.trig.player_id import PlayerId

_NUM_PLAYERS = 12
_PLAYER_SLOTS = [
    PlayerId.PLAYER_1,
    PlayerId.PLAYER_2,
    PlayerId.PLAYER_3,
    PlayerId.PLAYER_4,
    PlayerId.PLAYER_5,
    PlayerId.PLAYER_6,
    PlayerId.PLAYER_7,
    PlayerId.PLAYER_8,
    PlayerId.PLAYER_9,
    PlayerId.PLAYER_10,
    PlayerId.PLAYER_11,
    PlayerId.PLAYER_12,
]


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

    def set_all_player_types(
        self,
        player_types: dict[PlayerId, PlayerType],
        ownr: RichOwnrSection,
    ) -> RichOwnrSection:
        """Return a new section with all player types replaced.

        :param player_types: mapping from player slots to PlayerType; slots absent
            from the dict default to PlayerType.INACTIVE
        :param ownr: the existing OWNR section
        :return: new RichOwnrSection with the updated types
        """
        return RichOwnrSection(
            _player_types=[
                player_types.get(p, PlayerType.INACTIVE) for p in _PLAYER_SLOTS
            ]
        )
