"""Decode the WAV - WAV string IDs section.

Not Required.

Not Required.

There are 512 wav entries regardless of how many are actually used.

u32[512]: 1 long for each WAV. Indicates a string index is used for a WAV path in the
MPQ. If the entry is not used, it will be 0.
"""

from ....model.chk.wav.decoded_wav_section import DecodedWavSection
from ....model.chk.wav.wav_constants import MAX_WAV_FILES, UNUSED_WAV_STRING_ID
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....model.richchk.wav.rich_wav import RichWav
from ....model.richchk.wav.rich_wav_section import RichWavSection
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)
from ....util import logger


class RichChkWavTranscoder(
    RichChkSectionTranscoder[RichWavSection, DecodedWavSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedWavSection.section_name(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(RichWavSection.__name__)

    def decode(
        self,
        decoded_chk_section: DecodedWavSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichWavSection:
        wavs = []
        for index, string_id in enumerate(decoded_chk_section.wav_string_ids):
            if string_id != UNUSED_WAV_STRING_ID:
                wavs.append(
                    RichWav(
                        _path_in_chk=rich_chk_decode_context.rich_str_lookup.get_string_by_id(
                            string_id
                        ),
                        _index=index,
                    )
                )
        return RichWavSection(_wavs=wavs)

    def encode(
        self,
        rich_chk_section: RichWavSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedWavSection:
        string_ids = []
        wav_by_index = {wav.index: wav for wav in rich_chk_section.wavs}
        for wav_index in range(0, MAX_WAV_FILES):
            maybe_wav = wav_by_index.get(wav_index, None)
            if maybe_wav:
                string_ids.append(
                    rich_chk_encode_context.rich_str_lookup.get_id_by_string(
                        maybe_wav.path_in_chk
                    )
                )
            else:
                string_ids.append(UNUSED_WAV_STRING_ID)
        return DecodedWavSection(_wav_string_ids=string_ids)
