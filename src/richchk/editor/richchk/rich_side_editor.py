"""Editor for the SIDE - Player Races section."""

from ...model.richchk.side.player_race import PlayerRace
from ...model.richchk.side.rich_side_section import RichSideSection
from ...model.richchk.trig.player_id import PlayerId

_NUM_PLAYERS = 12


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

    def set_player_races(
        self,
        player_races: dict[PlayerId, PlayerRace],
        side: RichSideSection,
    ) -> RichSideSection:
        """Return a new section with the given player races updated.

        :param player_races: mapping of player slots to update; slots absent from the
            dict retain their existing race
        :param side: the existing SIDE section
        :return: new RichSideSection with the updated races
        """
        updated = list(side.player_races)
        for player, race in player_races.items():
            updated[player.id] = race
        return RichSideSection(_player_races=updated)
