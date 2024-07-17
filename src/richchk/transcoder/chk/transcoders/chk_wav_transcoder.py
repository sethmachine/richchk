"""Decode and encode the WAV section which contain WAV string IDs.

Not Required.

There are 512 wav entires regardless of how many are actually used.

u32[512]: 1 long for each WAV. Indicates a string index is used for a WAV path in the
MPQ. If the entry is not used, it will be 0.
"""

import struct
from io import BytesIO

from ....model.chk.wav.decoded_wav_section import DecodedWavSection
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder


class ChkWavTranscoder(
    ChkSectionTranscoder[DecodedWavSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedWavSection.section_name(),
):
    NUM_WAVS = 512

    def decode(self, chk_section_binary_data: bytes) -> DecodedWavSection:
        bytes_stream: BytesIO = BytesIO(chk_section_binary_data)
        string_ids = [
            struct.unpack("I", bytes_stream.read(4))[0] for _ in range(self.NUM_WAVS)
        ]
        return DecodedWavSection(_wav_string_ids=string_ids)

    def _encode(self, decoded_chk_section: DecodedWavSection) -> bytes:
        data: bytes = b""
        data += struct.pack(
            "{}I".format(self.NUM_WAVS), *decoded_chk_section.wav_string_ids
        )
        return data
