"""Decode MTXM."""

from ....model.chk.mtxm.decoded_mtxm_section import DecodedMtxmSection
from ....model.richchk.mtxm.rich_mtxm_section import RichMtxmSection
from ....model.richchk.mtxm.rich_tile import RichTile
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)
from ....util import logger


class RichMtxmTranscoder(
    RichChkSectionTranscoder[RichMtxmSection, DecodedMtxmSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedMtxmSection.section_name(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(RichMtxmTranscoder.__name__)

    def decode(
        self,
        decoded_chk_section: DecodedMtxmSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichMtxmSection:
        return RichMtxmSection(
            _tiles=[RichTile(_id=t) for t in decoded_chk_section.tiles],
        )

    def encode(
        self,
        rich_chk_section: RichMtxmSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedMtxmSection:
        result = DecodedMtxmSection(
            _tiles=tuple(t.id for t in rich_chk_section.tiles),
        )
        return result
