import logging
from typing import Any, Union

from ...model.chk.decoded_chk import DecodedChk
from ...model.chk.decoded_chk_section import DecodedChkSection
from ...model.chk.mrgn.decoded_mrgn_section import DecodedMrgnSection
from ...model.chk.str.decoded_str_section import DecodedStrSection
from ...model.chk.swnm.decoded_swnm_section import DecodedSwnmSection
from ...model.chk.unknown.decoded_unknown_section import DecodedUnknownSection
from ...model.richchk.mrgn.rich_mrgn_lookup import RichMrgnLookup
from ...model.richchk.mrgn.rich_mrgn_section import RichMrgnSection
from ...model.richchk.rich_chk import RichChk
from ...model.richchk.rich_chk_section import RichChkSection
from ...model.richchk.richchk_decode_context import RichChkDecodeContext
from ...model.richchk.richchk_encode_context import RichChkEncodeContext
from ...model.richchk.str.rich_str_lookup import RichStrLookup
from ...model.richchk.swnm.rich_swnm_lookup import RichSwnmLookup
from ...model.richchk.swnm.rich_swnm_section import RichSwnmSection
from ...transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ...transcoder.richchk.richchk_section_transcoder_factory import (
    RichChkSectionTranscoderFactory,
)
from ...transcoder.richchk.transcoders.rich_swnm_transcoder import RichChkSwnmTranscoder
from ...transcoder.richchk.transcoders.richchk_mrgn_transcoder import (
    RichChkMrgnTranscoder,
)
from ...util import logger
from ..util.chk_query_util import ChkQueryUtil
from .decoded_str_section_rebuilder import DecodedStrSectionRebuilder
from .lookups.mrgn.rich_mrgn_lookup_builder import RichMrgnLookupBuilder
from .lookups.mrgn.rich_mrgn_section_rebuilder import RichMrgnSectionRebuilder
from .lookups.swnm.rich_swnm_lookup_builder import RichSwnmLookupBuilder
from .lookups.swnm.rich_swnm_rebuilder import RichSwnmRebuilder
from .rich_str_lookup_builder import RichStrLookupBuilder


class RichChkIo:
    def __init__(self) -> None:
        self.log: logging.Logger = logger.get_logger(RichChkIo.__name__)

    def decode_chk(self, chk: DecodedChk) -> RichChk:
        decode_context = self._build_decode_context(chk)
        sections: list[Union[RichChkSection, DecodedChkSection]] = []
        for decoded_chk_section in chk.decoded_chk_sections:
            if isinstance(decoded_chk_section, DecodedUnknownSection):
                sections.append(decoded_chk_section)
            elif not RichChkSectionTranscoderFactory.supports_transcoding_chk_section(
                decoded_chk_section.section_name()
            ):
                sections.append(decoded_chk_section)
            else:
                transcoder: RichChkSectionTranscoder[
                    Any, Any
                ] = RichChkSectionTranscoderFactory.make_chk_section_transcoder(
                    decoded_chk_section.section_name()
                )
                sections.append(transcoder.decode(decoded_chk_section, decode_context))
        return RichChk(_chk_sections=sections)

    def encode_chk(self, rich_chk: RichChk) -> DecodedChk:
        # first need to iterate all relevant RichChk sections
        # and determine all new strings to add
        # then construct the new DecodedStrChk, plus
        new_str_section: DecodedStrSection = (
            DecodedStrSectionRebuilder.rebuild_str_section_from_rich_chk(rich_chk)
        )
        new_mrgn_section: RichMrgnSection = (
            RichMrgnSectionRebuilder.rebuild_rich_mrgn_section_from_rich_chk(rich_chk)
        )
        (
            new_swnm_section,
            swnm_lookup,
        ) = RichSwnmRebuilder.rebuild_rich_swnm_from_rich_chk(rich_chk)
        encode_context = self._build_encode_context(
            rich_chk, new_str_section, new_mrgn_section, swnm_lookup
        )
        was_swnm_added = False
        decoded_sections: list[DecodedChkSection] = []
        for chk_section in rich_chk.chk_sections:
            if isinstance(chk_section, DecodedUnknownSection):
                decoded_sections.append(chk_section)
            elif isinstance(chk_section, DecodedStrSection):
                # replace the old STR section
                # TODO: make an editor to replace sections by index or ID
                decoded_sections.append(new_str_section)
            elif isinstance(chk_section, DecodedChkSection):
                decoded_sections.append(chk_section)
            elif isinstance(
                chk_section, RichChkSection
            ) and RichChkSectionTranscoderFactory.supports_transcoding_chk_section(
                chk_section.section_name()
            ):
                transcoder: RichChkSectionTranscoder[
                    Any, Any
                ] = RichChkSectionTranscoderFactory.make_chk_section_transcoder(
                    chk_section.section_name()
                )
                if isinstance(chk_section, RichMrgnSection):
                    decoded_sections.append(
                        transcoder.encode(new_mrgn_section, encode_context)
                    )
                elif isinstance(chk_section, RichSwnmSection):
                    decoded_sections.append(
                        transcoder.encode(new_swnm_section, encode_context)
                    )
                    was_swnm_added = True
                else:
                    decoded_sections.append(
                        transcoder.encode(chk_section, encode_context)
                    )
            else:
                raise NotImplementedError(
                    f"RichChkSection {chk_section.section_name()} "
                    f"is not supported for encoding.  "
                    f"How did we decode it in the first place?"
                )
        if not was_swnm_added:
            self.log.info(
                "SWNM section is being added to CHK when it was not present before.  "
                "This likely means switch string data was edited."
            )
            decoded_sections.append(
                RichChkSwnmTranscoder().encode(new_swnm_section, encode_context)
            )
        return DecodedChk(_decoded_chk_sections=decoded_sections)

    def _build_decode_context(self, chk: DecodedChk) -> RichChkDecodeContext:
        rich_str_lookup = RichStrLookupBuilder().build_lookup(
            ChkQueryUtil.find_only_decoded_section_in_chk(DecodedStrSection, chk)
        )
        rich_mrgn = RichChkMrgnTranscoder().decode(
            decoded_chk_section=ChkQueryUtil.find_only_decoded_section_in_chk(
                DecodedMrgnSection, chk
            ),
            rich_chk_decode_context=RichChkDecodeContext(
                _rich_str_lookup=rich_str_lookup,
                _rich_mrgn_lookup=RichMrgnLookup(
                    _location_by_id_lookup={}, _id_by_location_lookup={}
                ),
            ),
        )
        return RichChkDecodeContext(
            _rich_str_lookup=rich_str_lookup,
            _rich_mrgn_lookup=RichMrgnLookupBuilder().build_lookup(rich_mrgn=rich_mrgn),
            _rich_swnm_lookup=self._build_rich_swnm_lookup_for_decode_context(
                chk, rich_str_lookup
            ),
        )

    def _build_rich_swnm_lookup_for_decode_context(
        self, chk: DecodedChk, rich_str_lookup: RichStrLookup
    ) -> RichSwnmLookup:
        try:
            swnm = ChkQueryUtil.find_only_decoded_section_in_chk(
                DecodedSwnmSection, chk
            )
            return RichSwnmLookupBuilder().build_lookup(
                decoded_swnm=swnm, rich_str_lookup=rich_str_lookup
            )
        except ValueError:
            self.log.info(
                "No SWNM section found in this CHK.  Returning an empty SWNM lookup."
            )
            return RichSwnmLookup(_switch_by_id_lookup={}, _id_by_switch_lookup={})

    def _build_encode_context(
        self,
        chk: RichChk,
        new_str_section: DecodedStrSection,
        new_mrgn_section: RichMrgnSection,
        swnm_lookup: RichSwnmLookup,
    ) -> RichChkEncodeContext:
        return RichChkEncodeContext(
            _rich_str_lookup=RichStrLookupBuilder().build_lookup(new_str_section),
            _rich_mrgn_lookup=RichMrgnLookupBuilder().build_lookup(new_mrgn_section),
            _rich_swnm_lookup=swnm_lookup,
        )
