"""Builds a RichSwnmLookup from a DecodedSwnmSection and RichStrLookup."""

import logging

from .....model.chk.swnm.decoded_swnm_section import DecodedSwnmSection
from .....model.richchk.str.rich_str_lookup import RichStrLookup
from .....model.richchk.swnm.rich_switch import RichSwitch
from .....model.richchk.swnm.rich_swnm_lookup import RichSwnmLookup
from .....util import logger


class RichSwnmLookupBuilder:
    def __init__(self) -> None:
        self.log: logging.Logger = logger.get_logger(RichSwnmLookupBuilder.__name__)

    def build_lookup(
        self, decoded_swnm: DecodedSwnmSection, rich_str_lookup: RichStrLookup
    ) -> RichSwnmLookup:
        location_by_id = {}
        for switch_id, string_id in enumerate(decoded_swnm.switch_string_ids):
            location_by_id[switch_id] = RichSwitch(
                _custom_name=rich_str_lookup.get_string_by_id(string_id),
                _index=switch_id,
            )
        return RichSwnmLookup(
            _switch_by_id_lookup=location_by_id, _id_by_switch_lookup={}
        )
