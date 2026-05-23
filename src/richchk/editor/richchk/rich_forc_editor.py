"""Editor for the FORC - Force Settings section."""

from ...model.richchk.forc.force_id import ForceId
from ...model.richchk.forc.rich_forc_section import RichForcSection
from ...model.richchk.forc.rich_force import RichForce
from ...model.richchk.trig.player_id import PlayerId

_NUM_PLAYERS = 8


class RichForcEditor:
    def add_player_to_force(
        self,
        player: PlayerId,
        force: ForceId,
        forc: RichForcSection,
    ) -> RichForcSection:
        """Return a new section with one player's force assignment updated.

        :param player: the player slot to update
        :param force: the force to assign the player to
        :param forc: the existing FORC section
        :return: new RichForcSection with the updated assignment
        """
        if player.id >= _NUM_PLAYERS:
            raise ValueError(
                f"player must be one of PLAYER_1 through PLAYER_8, got {player}"
            )
        updated = list(forc.player_force_assignments)
        updated[player.id] = force
        return RichForcSection(
            _player_force_assignments=updated,
            _forces=forc.forces,
        )

    def update_force(
        self,
        force: ForceId,
        rich_force: RichForce,
        forc: RichForcSection,
    ) -> RichForcSection:
        """Return a new section with one force's name and flags replaced.

        :param force: which force slot to update
        :param rich_force: the replacement RichForce
        :param forc: the existing FORC section
        :return: new RichForcSection with the updated force
        """
        updated_forces = list(forc.forces)
        updated_forces[force.id] = rich_force
        return RichForcSection(
            _player_force_assignments=forc.player_force_assignments,
            _forces=updated_forces,
        )
