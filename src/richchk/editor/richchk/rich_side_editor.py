"""Editor for the SIDE - Player Races section."""

from ...model.richchk.side.player_race import PlayerRace
from ...model.richchk.side.rich_side_section import RichSideSection

_NUM_PLAYERS = 12


class RichSideEditor:
    def set_player_race(
        self,
        player_slot: int,
        race: PlayerRace,
        side: RichSideSection,
    ) -> RichSideSection:
        """Return a new section with the race for a single player slot replaced.

        :param player_slot: zero-based player slot index (0-11)
        :param race: the PlayerRace to assign
        :param side: the existing SIDE section
        :return: new RichSideSection with the updated race
        """
        if player_slot < 0 or player_slot >= _NUM_PLAYERS:
            raise ValueError(
                f"player_slot must be in range [0, {_NUM_PLAYERS - 1}], got {player_slot}"
            )
        updated = list(side.player_races)
        updated[player_slot] = race
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
