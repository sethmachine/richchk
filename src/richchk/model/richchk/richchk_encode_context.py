"""Contains all the global CHK context needed to produce DecodedChk from RichChk
representations."""

import dataclasses
from typing import Optional

from ...model.richchk.mrgn.rich_mrgn_lookup import RichMrgnLookup
from ...model.richchk.str.rich_str_lookup import RichStrLookup
from .swnm.rich_swnm_lookup import RichSwnmLookup
from .uprp.rich_cuwp_lookup import RichCuwpLookup
from .wav.rich_wav_metadata_lookup import RichWavMetadataLookup


@dataclasses.dataclass(frozen=True)
class RichChkEncodeContext:
    _rich_str_lookup: RichStrLookup
    _rich_mrgn_lookup: RichMrgnLookup
    _rich_swnm_lookup: RichSwnmLookup
    _rich_cuwp_lookup: RichCuwpLookup
    # this is only present when a RichChk is edited via StacraftMpqIo
    _wav_metadata_lookup: Optional[RichWavMetadataLookup] = None

    @property
    def rich_str_lookup(self) -> RichStrLookup:
        return self._rich_str_lookup

    @property
    def rich_mrgn_lookup(self) -> RichMrgnLookup:
        return self._rich_mrgn_lookup

    @property
    def rich_swnm_lookup(self) -> RichSwnmLookup:
        return self._rich_swnm_lookup

    @property
    def rich_cuwp_lookup(self) -> RichCuwpLookup:
        return self._rich_cuwp_lookup

    @property
    def wav_metadata_lookup(self) -> Optional[RichWavMetadataLookup]:
        return self._wav_metadata_lookup
