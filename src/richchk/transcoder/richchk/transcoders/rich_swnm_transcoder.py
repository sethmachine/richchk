"""Decode the SWNM - Switch names section.

Not Required.

This section contains the strings used for each switch. There are 256 switches, and
can't be any more or any less.

u32[256]: One long for each switch, specifies the string number for the name of each
switch. Unnamed switches will have an index of 0, and have a default switch name.
"""

from ....model.chk.swnm.decoded_swnm_section import DecodedSwnmSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....model.richchk.swnm.rich_swnm_section import RichSwnmSection
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)
from ....util import logger


class RichChkSwnmTranscoder(
    RichChkSectionTranscoder[RichSwnmSection, DecodedSwnmSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedSwnmSection.section_name(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(RichChkSwnmTranscoder.__name__)

    def decode(
        self,
        decoded_chk_section: DecodedSwnmSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichSwnmSection:
        switches = []
        for switch_id, _ in enumerate(decoded_chk_section.switch_string_ids):
            maybe_switch = rich_chk_decode_context.rich_swnm_lookup.get_switch_by_id(
                switch_id
            )
            if maybe_switch:
                switches.append(maybe_switch)
            else:
                msg = (
                    f"No entry for switch with ID {switch_id} in RichSwnmLookup!  "
                    f"All switch IDs should be accounted for."
                )
                self.log.error(msg)
                raise KeyError(msg)
        return RichSwnmSection(_switches=switches)

    def encode(
        self,
        rich_chk_section: RichSwnmSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedSwnmSection:
        string_ids = []
        for switch in rich_chk_section.switches:
            # 0 is returned if there's no custom name for the switch
            string_ids.append(
                rich_chk_encode_context.rich_str_lookup.get_id_by_string(
                    switch.custom_name
                )
            )
        return DecodedSwnmSection(_switch_string_ids=string_ids)
