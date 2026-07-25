"""Editor for the PTEx - Brood War Tech Restrictions section."""

from ...model.richchk.ptex.rich_ptex_section import RichPtexSection
from ...model.richchk.techs.tech_id import TechId
from ...model.richchk.trig.player_id import PlayerId


class RichPtexEditor:
    def set_tech_available_for_player(
        self,
        player: PlayerId,
        tech: TechId,
        available: bool,
        ptex: RichPtexSection,
    ) -> RichPtexSection:
        """Return a new section with the tech availability for a player updated.

        :param player: the player slot to update
        :param tech: the tech to update
        :param available: True=available, False=unavailable
        :param ptex: the existing PTEx section
        :return: new RichPtexSection with the updated availability
        """
        updated = {p: dict(techs) for p, techs in ptex.player_tech_availability.items()}
        updated[player][tech] = available
        updated_defaults = {
            p: dict(techs) for p, techs in ptex.player_uses_defaults.items()
        }
        updated_defaults[player][tech] = False
        return RichPtexSection(
            _player_tech_availability=updated,
            _player_tech_researched=ptex.player_tech_researched,
            _global_tech_availability=ptex.global_tech_availability,
            _global_tech_researched=ptex.global_tech_researched,
            _player_uses_defaults=updated_defaults,
        )

    def set_tech_researched_for_player(
        self,
        player: PlayerId,
        tech: TechId,
        is_researched: bool,
        ptex: RichPtexSection,
    ) -> RichPtexSection:
        """Return a new section with the tech researched state for a player updated.

        :param player: the player slot to update
        :param tech: the tech to update
        :param is_researched: True=already researched, False=not researched
        :param ptex: the existing PTEx section
        :return: new RichPtexSection with the updated researched state
        """
        updated = {p: dict(techs) for p, techs in ptex.player_tech_researched.items()}
        updated[player][tech] = is_researched
        updated_defaults = {
            p: dict(techs) for p, techs in ptex.player_uses_defaults.items()
        }
        updated_defaults[player][tech] = False
        return RichPtexSection(
            _player_tech_availability=ptex.player_tech_availability,
            _player_tech_researched=updated,
            _global_tech_availability=ptex.global_tech_availability,
            _global_tech_researched=ptex.global_tech_researched,
            _player_uses_defaults=updated_defaults,
        )

    def set_player_uses_default(
        self,
        player: PlayerId,
        tech: TechId,
        uses_default: bool,
        ptex: RichPtexSection,
    ) -> RichPtexSection:
        """Return a new section with the uses-default flag for a player/tech updated.

        :param player: the player slot to update
        :param tech: the tech to update
        :param uses_default: True=use global default, False=use player override
        :param ptex: the existing PTEx section
        :return: new RichPtexSection with the updated flag
        """
        updated = {p: dict(techs) for p, techs in ptex.player_uses_defaults.items()}
        updated[player][tech] = uses_default
        return RichPtexSection(
            _player_tech_availability=ptex.player_tech_availability,
            _player_tech_researched=ptex.player_tech_researched,
            _global_tech_availability=ptex.global_tech_availability,
            _global_tech_researched=ptex.global_tech_researched,
            _player_uses_defaults=updated,
        )

    def apply_player_tech_availability(
        self,
        updates: dict[PlayerId, dict[TechId, bool]],
        ptex: RichPtexSection,
    ) -> RichPtexSection:
        """Return a new section with per-player tech availability merged from a partial
        dict.

        Only the (player, tech) pairs present in `updates` are changed; all others are
        left as-is.  player_uses_defaults is set to False for each pair so the per-
        player value is consulted at runtime.

        :param updates: sparse mapping of player -> {tech -> available}
        :param ptex: the existing PTEx section
        :return: new RichPtexSection with the merged overrides applied
        """
        new_availability = {
            p: dict(techs) for p, techs in ptex.player_tech_availability.items()
        }
        new_defaults = {
            p: dict(techs) for p, techs in ptex.player_uses_defaults.items()
        }
        for player, tech_map in updates.items():
            for tech, available in tech_map.items():
                new_availability[player][tech] = available
                new_defaults[player][tech] = False
        return RichPtexSection(
            _player_tech_availability=new_availability,
            _player_tech_researched=ptex.player_tech_researched,
            _global_tech_availability=ptex.global_tech_availability,
            _global_tech_researched=ptex.global_tech_researched,
            _player_uses_defaults=new_defaults,
        )

    def apply_player_tech_researched(
        self,
        updates: dict[PlayerId, dict[TechId, bool]],
        ptex: RichPtexSection,
    ) -> RichPtexSection:
        """Return a new section with per-player tech researched state merged from a
        partial dict.

        Only the (player, tech) pairs present in `updates` are changed; all others are
        left as-is.  player_uses_defaults is set to False for each pair so the per-
        player value is consulted at runtime.

        :param updates: sparse mapping of player -> {tech -> is_researched}
        :param ptex: the existing PTEx section
        :return: new RichPtexSection with the merged overrides applied
        """
        new_researched = {
            p: dict(techs) for p, techs in ptex.player_tech_researched.items()
        }
        new_defaults = {
            p: dict(techs) for p, techs in ptex.player_uses_defaults.items()
        }
        for player, tech_map in updates.items():
            for tech, is_researched in tech_map.items():
                new_researched[player][tech] = is_researched
                new_defaults[player][tech] = False
        return RichPtexSection(
            _player_tech_availability=ptex.player_tech_availability,
            _player_tech_researched=new_researched,
            _global_tech_availability=ptex.global_tech_availability,
            _global_tech_researched=ptex.global_tech_researched,
            _player_uses_defaults=new_defaults,
        )
