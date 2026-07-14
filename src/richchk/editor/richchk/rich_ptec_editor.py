"""Editor for the PTEC - Classic Tech Restrictions section."""

from ...model.richchk.ptec.rich_ptec_section import RichPtecSection
from ...model.richchk.techs.tech_id import TechId
from ...model.richchk.trig.player_id import PlayerId

_NUM_PLAYERS = 12
_NUM_TECHS = 24


class RichPtecEditor:
    def set_tech_available_for_player(
        self,
        player: PlayerId,
        tech: TechId,
        available: bool,
        ptec: RichPtecSection,
    ) -> RichPtecSection:
        """Return a new section with the tech availability for a player updated.

        :param player: the player slot to update (PLAYER_1 through PLAYER_12)
        :param tech: the tech to update (must have id < 24)
        :param available: True=available, False=unavailable
        :param ptec: the existing PTEC section
        :return: new RichPtecSection with the updated availability
        """
        if player.id >= _NUM_PLAYERS:
            raise ValueError(
                f"player must be one of PLAYER_1 through PLAYER_12, got {player}"
            )
        if tech.id >= _NUM_TECHS:
            raise ValueError(f"tech id must be < {_NUM_TECHS}, got {tech}")
        updated = [row.copy() for row in ptec.player_tech_availability]
        updated[player.id][tech.id] = available
        return RichPtecSection(
            _player_tech_availability=updated,
            _player_tech_researched=ptec.player_tech_researched,
            _global_tech_availability=ptec.global_tech_availability,
            _global_tech_researched=ptec.global_tech_researched,
            _player_uses_defaults=ptec.player_uses_defaults,
        )

    def set_tech_researched_for_player(
        self,
        player: PlayerId,
        tech: TechId,
        researched: bool,
        ptec: RichPtecSection,
    ) -> RichPtecSection:
        """Return a new section with the tech researched state for a player updated.

        :param player: the player slot to update (PLAYER_1 through PLAYER_12)
        :param tech: the tech to update (must have id < 24)
        :param researched: True=already researched, False=not researched
        :param ptec: the existing PTEC section
        :return: new RichPtecSection with the updated researched state
        """
        if player.id >= _NUM_PLAYERS:
            raise ValueError(
                f"player must be one of PLAYER_1 through PLAYER_12, got {player}"
            )
        if tech.id >= _NUM_TECHS:
            raise ValueError(f"tech id must be < {_NUM_TECHS}, got {tech}")
        updated = [row.copy() for row in ptec.player_tech_researched]
        updated[player.id][tech.id] = researched
        return RichPtecSection(
            _player_tech_availability=ptec.player_tech_availability,
            _player_tech_researched=updated,
            _global_tech_availability=ptec.global_tech_availability,
            _global_tech_researched=ptec.global_tech_researched,
            _player_uses_defaults=ptec.player_uses_defaults,
        )

    def set_player_uses_default(
        self,
        player: PlayerId,
        tech: TechId,
        uses_default: bool,
        ptec: RichPtecSection,
    ) -> RichPtecSection:
        """Return a new section with the uses-default flag for a player/tech updated.

        :param player: the player slot to update (PLAYER_1 through PLAYER_12)
        :param tech: the tech to update (must have id < 24)
        :param uses_default: True=use global default, False=use player override
        :param ptec: the existing PTEC section
        :return: new RichPtecSection with the updated flag
        """
        if player.id >= _NUM_PLAYERS:
            raise ValueError(
                f"player must be one of PLAYER_1 through PLAYER_12, got {player}"
            )
        if tech.id >= _NUM_TECHS:
            raise ValueError(f"tech id must be < {_NUM_TECHS}, got {tech}")
        updated = [row.copy() for row in ptec.player_uses_defaults]
        updated[player.id][tech.id] = uses_default
        return RichPtecSection(
            _player_tech_availability=ptec.player_tech_availability,
            _player_tech_researched=ptec.player_tech_researched,
            _global_tech_availability=ptec.global_tech_availability,
            _global_tech_researched=ptec.global_tech_researched,
            _player_uses_defaults=updated,
        )
