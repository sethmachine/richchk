"""Builds a RichSwnmLookup from a DecodedSwnmSection and RichStrLookup."""

import logging

from .....model.chk.uprp.decoded_uprp_section import DecodedUprpSection
from .....model.richchk.richchk_decode_context import RichChkDecodeContext
from .....model.richchk.uprp.rich_cuwp_lookup import RichCuwpLookup
from .....model.richchk.uprp.rich_uprp_section import RichUprpSection
from .....transcoder.richchk.transcoders.richchk_uprp_transcoder import (
    RichChkUprpTranscoder,
)
from .....util import logger


class RichCuwpLookupBuilder:
    def __init__(self) -> None:
        self.log: logging.Logger = logger.get_logger(RichCuwpLookupBuilder.__name__)

    def build_lookup(
        self,
        decoded_uprp: DecodedUprpSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichCuwpLookup:
        rich_uprp = RichChkUprpTranscoder().decode(
            decoded_uprp, rich_chk_decode_context
        )
        return self.build_lookup_from_rich_uprp(rich_uprp)

    def build_lookup_from_rich_uprp(self, rich_uprp: RichUprpSection) -> RichCuwpLookup:
        cuwp_by_id = {}
        id_by_cuwp = {}
        for cuwp in rich_uprp.cuwp_slots:
            assert cuwp.index is not None
            cuwp_by_id[cuwp.index] = cuwp
            id_by_cuwp[cuwp] = cuwp.index
        return RichCuwpLookup(
            _cuwp_by_id_lookup=cuwp_by_id, _id_by_cuwp_lookup=id_by_cuwp
        )
