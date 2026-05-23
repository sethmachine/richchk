"""Decode and encode the OWNR - StarCraft Player Types section."""

from ....model.chk.ownr.decoded_ownr_section import DecodedOwnrSection
from ....model.richchk.ownr.player_type import PlayerType
from ....model.richchk.ownr.rich_ownr_section import RichOwnrSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)
from ....transcoder.richchk.transcoders.helpers.richchk_enum_transcoder import (
    RichChkEnumTranscoder,
)


class RichOwnrTranscoder(
    RichChkSectionTranscoder[RichOwnrSection, DecodedOwnrSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedOwnrSection.section_name(),
):
    def decode(
        self,
        decoded_chk_section: DecodedOwnrSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichOwnrSection:
        return RichOwnrSection(
            _player_types=[
                RichChkEnumTranscoder.decode_enum(type_id, PlayerType)
                for type_id in decoded_chk_section.player_controllers
            ]
        )

    def encode(
        self,
        rich_chk_section: RichOwnrSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedOwnrSection:
        return DecodedOwnrSection(
            _player_controllers=[
                RichChkEnumTranscoder.encode_enum(player_type)
                for player_type in rich_chk_section.player_types
            ]
        )
