"""Decode and encode the SIDE - Player Races section."""

from ....model.chk.side.decoded_side_section import DecodedSideSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....model.richchk.side.player_race import PlayerRace
from ....model.richchk.side.rich_side_section import RichSideSection
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)
from ....transcoder.richchk.transcoders.helpers.richchk_enum_transcoder import (
    RichChkEnumTranscoder,
)


class RichSideTranscoder(
    RichChkSectionTranscoder[RichSideSection, DecodedSideSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedSideSection.section_name(),
):
    def decode(
        self,
        decoded_chk_section: DecodedSideSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichSideSection:
        return RichSideSection(
            _player_races=[
                RichChkEnumTranscoder.decode_enum(race_id, PlayerRace)
                for race_id in decoded_chk_section.player_races
            ]
        )

    def encode(
        self,
        rich_chk_section: RichSideSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedSideSection:
        return DecodedSideSection(
            _player_races=[
                RichChkEnumTranscoder.encode_enum(race)
                for race in rich_chk_section.player_races
            ]
        )
