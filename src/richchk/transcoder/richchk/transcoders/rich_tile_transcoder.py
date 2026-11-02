"""Decode TILE."""

from ....model.chk.tile.decoded_tile_section import DecodedTileSection
from ....model.richchk.mtxm.rich_tile import RichTile
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....model.richchk.tile.rich_tile_section import RichTileSection
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)
from ....util import logger


class RichTileTranscoder(
    RichChkSectionTranscoder[RichTileSection, DecodedTileSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedTileSection.section_name(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(RichTileTranscoder.__name__)

    def decode(
        self,
        decoded_chk_section: DecodedTileSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichTileSection:
        return RichTileSection(
            _tiles=[RichTile(_id=t) for t in decoded_chk_section.tiles],
        )

    def encode(
        self,
        rich_chk_section: RichTileSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTileSection:
        result = DecodedTileSection(
            _tiles=tuple(t.id for t in rich_chk_section.tiles),
        )
        return result
