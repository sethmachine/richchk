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

    def set_all_player_races(
        self,
        races: list[PlayerRace],
        side: RichSideSection,
    ) -> RichSideSection:
        """Return a new section with all player races replaced.

        :param races: list of exactly 12 PlayerRace values
        :param side: the existing SIDE section
        :return: new RichSideSection with the updated races
        """
        if len(races) != _NUM_PLAYERS:
            raise ValueError(
                f"races must have exactly {_NUM_PLAYERS} entries, got {len(races)}"
            )
        return RichSideSection(_player_races=list(races))
