"""Editor for the FORC - Force Settings section."""

from ...model.richchk.forc.force_flags import ForceFlags
from ...model.richchk.forc.rich_forc_section import RichForcSection
from ...model.richchk.forc.rich_force import RichForce

_NUM_PLAYERS = 8
_NUM_FORCES = 4


class RichForcEditor:
    def set_player_force_assignment(
        self,
        player_slot: int,
        force_index: int,
        forc: RichForcSection,
    ) -> RichForcSection:
        """Return a new section with one player's force assignment updated.

        :param player_slot: zero-based player slot index (0-7)
        :param force_index: force index to assign (0-3)
        :param forc: the existing FORC section
        :return: new RichForcSection with the updated assignment
        """
        if player_slot < 0 or player_slot >= _NUM_PLAYERS:
            raise ValueError(
                f"player_slot must be in range [0, {_NUM_PLAYERS - 1}], got {player_slot}"
            )
        if force_index < 0 or force_index >= _NUM_FORCES:
            raise ValueError(
                f"force_index must be in range [0, {_NUM_FORCES - 1}], got {force_index}"
            )
        updated = list(forc.player_force_assignments)
        updated[player_slot] = force_index
        return RichForcSection(
            _player_force_assignments=updated,
            _forces=forc.forces,
        )

    def update_force(
        self,
        force_index: int,
        force: RichForce,
        forc: RichForcSection,
    ) -> RichForcSection:
        """Return a new section with one force's name and flags replaced.

        :param force_index: zero-based force index (0-3)
        :param force: the replacement RichForce
        :param forc: the existing FORC section
        :return: new RichForcSection with the updated force
        """
        if force_index < 0 or force_index >= _NUM_FORCES:
            raise ValueError(
                f"force_index must be in range [0, {_NUM_FORCES - 1}], got {force_index}"
            )
        updated_forces = list(forc.forces)
        updated_forces[force_index] = force
        return RichForcSection(
            _player_force_assignments=forc.player_force_assignments,
            _forces=updated_forces,
        )

    def set_force_flags(
        self,
        force_index: int,
        flags: ForceFlags,
        forc: RichForcSection,
    ) -> RichForcSection:
        """Return a new section with the flags for one force replaced.

        :param force_index: zero-based force index (0-3)
        :param flags: the replacement ForceFlags
        :param forc: the existing FORC section
        :return: new RichForcSection with the updated flags
        """
        if force_index < 0 or force_index >= _NUM_FORCES:
            raise ValueError(
                f"force_index must be in range [0, {_NUM_FORCES - 1}], got {force_index}"
            )
        updated_forces = list(forc.forces)
        old_force = updated_forces[force_index]
        updated_forces[force_index] = RichForce(_name=old_force.name, _flags=flags)
        return RichForcSection(
            _player_force_assignments=forc.player_force_assignments,
            _forces=updated_forces,
        )
