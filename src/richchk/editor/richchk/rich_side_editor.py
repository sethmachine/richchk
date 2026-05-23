"""Editor for the SIDE - Player Races section."""

from ...model.richchk.side.player_race import PlayerRace
from ...model.richchk.side.rich_side_section import RichSideSection
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


class RichSideEditor:
    def set_player_race(
        self,
        player: PlayerId,
        race: PlayerRace,
        side: RichSideSection,
    ) -> RichSideSection:
        """Return a new section with the race for a single player slot replaced.

        :param player: the player slot to update (PLAYER_1 through PLAYER_12)
        :param race: the PlayerRace to assign
        :param side: the existing SIDE section
        :return: new RichSideSection with the updated race
        """
        if player.id >= _NUM_PLAYERS:
            raise ValueError(
                f"player must be one of PLAYER_1 through PLAYER_12, got {player}"
            )
        updated = list(side.player_races)
        updated[player.id] = race
        return RichSideSection(_player_races=updated)

    def set_all_player_races(
        self,
        player_races: dict[PlayerId, PlayerRace],
        side: RichSideSection,
    ) -> RichSideSection:
        """Return a new section with all player races replaced.

        :param player_races: mapping from player slots to PlayerRace; slots absent
            from the dict default to PlayerRace.USER_SELECT
        :param side: the existing SIDE section
        :return: new RichSideSection with the updated races
        """
        return RichSideSection(
            _player_races=[
                player_races.get(p, PlayerRace.USER_SELECT) for p in _PLAYER_SLOTS
            ]
        )
