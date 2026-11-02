"""Decode and encode the PTEC - Classic Tech Restrictions section."""


from ....model.chk.ptec.decoded_ptec_section import DecodedPtecSection
from ....model.richchk.ptec.rich_ptec_section import RichPtecSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....model.richchk.techs.tech_id import TechId
from ....model.richchk.trig.player_id import PlayerId
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)

_GAME_PLAYERS = [p for p in PlayerId if p.id < 12]
_CLASSIC_TECHS = [t for t in TechId if t.id < 24]

_NUM_TECHS = 24


class RichPtecTranscoder(
    RichChkSectionTranscoder[RichPtecSection, DecodedPtecSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedPtecSection.section_name(),
):
    def decode(
        self,
        decoded_chk_section: DecodedPtecSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichPtecSection:
        player_avail = {
            player: {
                tech: bool(
                    decoded_chk_section.player_tech_availability[
                        player.id * _NUM_TECHS + tech.id
                    ]
                )
                for tech in _CLASSIC_TECHS
            }
            for player in _GAME_PLAYERS
        }
        player_researched = {
            player: {
                tech: bool(
                    decoded_chk_section.player_tech_researched[
                        player.id * _NUM_TECHS + tech.id
                    ]
                )
                for tech in _CLASSIC_TECHS
            }
            for player in _GAME_PLAYERS
        }
        global_avail = {
            tech: bool(decoded_chk_section.global_tech_availability[tech.id])
            for tech in _CLASSIC_TECHS
        }
        global_researched = {
            tech: bool(decoded_chk_section.global_tech_researched[tech.id])
            for tech in _CLASSIC_TECHS
        }
        player_defaults = {
            player: {
                tech: bool(
                    decoded_chk_section.player_uses_defaults[
                        player.id * _NUM_TECHS + tech.id
                    ]
                )
                for tech in _CLASSIC_TECHS
            }
            for player in _GAME_PLAYERS
        }
        return RichPtecSection(
            _player_tech_availability=player_avail,
            _player_tech_researched=player_researched,
            _global_tech_availability=global_avail,
            _global_tech_researched=global_researched,
            _player_uses_defaults=player_defaults,
        )

    def encode(
        self,
        rich_chk_section: RichPtecSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedPtecSection:
        flat_avail = [0] * (12 * _NUM_TECHS)
        for player, techs in rich_chk_section.player_tech_availability.items():
            for tech, avail in techs.items():
                flat_avail[player.id * _NUM_TECHS + tech.id] = int(avail)
        flat_researched = [0] * (12 * _NUM_TECHS)
        for player, techs in rich_chk_section.player_tech_researched.items():
            for tech, is_researched in techs.items():
                flat_researched[player.id * _NUM_TECHS + tech.id] = int(is_researched)
        global_avail = [0] * _NUM_TECHS
        for tech, avail in rich_chk_section.global_tech_availability.items():
            global_avail[tech.id] = int(avail)
        global_researched = [0] * _NUM_TECHS
        for tech, is_researched in rich_chk_section.global_tech_researched.items():
            global_researched[tech.id] = int(is_researched)
        flat_defaults = [0] * (12 * _NUM_TECHS)
        for player, techs in rich_chk_section.player_uses_defaults.items():
            for tech, uses_default in techs.items():
                flat_defaults[player.id * _NUM_TECHS + tech.id] = int(uses_default)
        result = DecodedPtecSection(
            _player_tech_availability=flat_avail,
            _player_tech_researched=flat_researched,
            _global_tech_availability=global_avail,
            _global_tech_researched=global_researched,
            _player_uses_defaults=flat_defaults,
        )
        return result
