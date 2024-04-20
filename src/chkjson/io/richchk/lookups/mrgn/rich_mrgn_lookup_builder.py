"""Builds a RichMrgnLookup from a DecodedMrgnSection.

The lookup is used to resolve location IDs to actual location data for human readability
in the RichChk representation.
"""

import logging

from .....model.chk.mrgn.decoded_mrgn_section import DecodedMrgnSection
from .....model.richchk.mrgn.rich_mrgn_lookup import RichMrgnLookup
from .....model.richchk.richchk_decode_context import RichChkDecodeContext
from .....transcoder.richchk.transcoders.richchk_mrgn_transcoder import (
    RichChkMrgnTranscoder,
)
from .....util import logger


class RichMrgnLookupBuilder:
    def __init__(self) -> None:
        self.log: logging.Logger = logger.get_logger(RichMrgnLookupBuilder.__name__)

    def build_lookup(
        self,
        decoded_mrgn: DecodedMrgnSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichMrgnLookup:
        transcoder: RichChkMrgnTranscoder = RichChkMrgnTranscoder()
        rich_mrgn = transcoder.decode(decoded_mrgn, rich_chk_decode_context)
        location_by_id = {}
        for id_, location in enumerate(rich_mrgn.locations):
            # string IDs are 1-indexed (0 denotes no string used)
            actual_location_id = id_ + 1
            location_by_id[actual_location_id] = location
        return RichMrgnLookup(_location_by_id_lookup=location_by_id)
